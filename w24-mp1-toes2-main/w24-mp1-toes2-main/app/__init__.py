from os import environ, path
from flask import Flask, g, session, request, render_template, url_for, redirect
from secrets import token_hex
from sqlite3 import connect as connectToDB, Row, PARSE_COLNAMES, PARSE_DECLTYPES
from .db import DB
from .query import Query
from .models.member import Member
from .models.borrowing import Borrowing
from .models.review import Review
from .models import view_models
from datetime import date

app = Flask(__name__)
app.secret_key = token_hex()


def getDBConnection():
    connection = getattr(g, "_database", None)
    if connection is None:
        if "APP_DB_PATH" not in environ:
            print("DB path not found. Exiting...")
            exit(1)
        else:
            connection = g._database = connectToDB(environ["APP_DB_PATH"],
                                                   detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            connection.row_factory = Row

            # Add trigger code to any database given
            packagePath = path.dirname(path.abspath(__file__))
            pathToTriggerCode = path.join(
                packagePath, "util", "penalty_trigger.sql")
            with open(pathToTriggerCode) as triggerSQL:
                cursor = connection.cursor()
                cursor.execute(triggerSQL.read())

    return connection


@app.teardown_appcontext
def closeDBConnection(exception):
    connection = getattr(g, '_database', None)
    if connection is not None:
        connection.close()


def isLoggedIn() -> bool:
    return "email" in session


@app.route("/")
def index():
    if isLoggedIn():
        return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))


@app.route("/profile", methods=["POST", "GET"])
def profile():
    member = None

    db = DB(getDBConnection())
    query = Query(db)

    # POST
    if request.method == "POST" and not isLoggedIn():
        postData = request.form.to_dict()
        # Register page
        if postData.keys() >= {"email", "name", "byear", "faculty", "passwd"}:
            userAlreadyExists = query.userExists(postData["email"])
            if not userAlreadyExists:
                member = Member.createFrom(postData)
                successfulInsertion = db.insert(member)
                if not successfulInsertion:
                    return redirect(url_for("register", error="Registration Failed"))
                else:
                    session["email"] = member.email
            else:
                return redirect(url_for("register", error="User already exists"))
        # Login page
        elif postData.keys() >= {"email", "passwd"}:
            email, passwd = postData["email"], postData["passwd"]
            correctLogin = query.checkLogin(email=email, password=passwd)
            if not correctLogin:
                return redirect(url_for("login", error="Invalid email or password"))
            else:
                session["email"] = email
                member = query.getMember(email)
    # GET request
    else:
        if isLoggedIn():
            member = query.getMember(session["email"])
        else:
            return redirect(url_for("register"))

    profileInfo = view_models.Profile(
        member=member,
        borrowCounts=query.getBorrowCounts(member.email),
        unpaidPenaltyCount=len(query.getUnpaidPenalties(member.email)),
        totalDebt=query.getDebt(member.email)
    )
    return render_template("profile.html", profile=profileInfo)


@app.route("/return", methods=["GET", "POST"])
def borrowings():
    if not isLoggedIn():
        return redirect(url_for("login"))

    db = DB(getDBConnection())
    query = Query(db)
    email = session["email"]

    if request.method == "POST":
        if "bid" in request.form and request.form.get("bid") is not None:
            bid = int(request.form["bid"].strip())
            successfulUpdate = db.updateColumn(column="end_date", value=date.today(), table="borrowings",
                                               where="bid=? AND member=?", whereParams=(bid, email),
                                               increment=False)
            if successfulUpdate:
                if request.form.keys() >= {"rating", "rtext"}:
                    bookID = query.getBorrowing(bid).bookID
                    rating = int(request.form["rating"].strip())
                    text = request.form["rtext"].strip()
                    newReview = Review(rid=None, bookID=bookID, member=email,
                                       rating=rating, text=text)

                    successfulInsertion = db.insert(newReview)
                    if not successfulInsertion:
                        print("Error: Unable to insert review to database")
            else:
                print("Error: Unable to update borrowings table")

        elif "book_id" in request.form:
            bookID = request.form.get("book_id").strip()
            if bookID is not None:
                title = query.getBookTitle(int(bookID))
                newBorrowing = Borrowing(bid=None, member=email, bookID=bookID,
                                         bookTitle=title, startDate=date.today(), endDate=None)
                successfulInsertion = db.insert(newBorrowing)
                if not successfulInsertion:
                    print("Error: Unable to insert borrowing into DB")

    borrowingsList = query.getCurrentBorrowings(email)
    return render_template("return.html", borrowings=borrowingsList)


@app.route("/penalty", methods=["GET", "POST"])
def penalties():
    if not isLoggedIn():
        return redirect(url_for("login"))

    email = session["email"]
    db = DB(getDBConnection())

    if request.method == "POST":
        if request.form.keys() >= {"payment", "pid"}:
            pid = int(request.form.get("pid").strip())
            payment = int(request.form.get("payment").strip())

            if pid is not None and payment is not None:
                db.updateColumn(column="paid_amount", value=payment, increment=True,
                                table="penalties", where="pid=?", whereParams=(pid,))

    query = Query(db)
    return render_template("penalty.html", penalties=query.getUnpaidPenalties(email))


@app.route("/register")
def register():
    if isLoggedIn():
        return redirect(url_for("profile"))
    return render_template("register.html")


@app.route("/login")
def login():
    if isLoggedIn():
        return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/search")
def search():
    if not isLoggedIn():
        return redirect(url_for("login"))

    query = Query(DB(getDBConnection()))
    searchItems = query.search(request.args.get("query", ""),
                               int(request.args.get("limit", 5)))

    return render_template("search.html", items=searchItems)


@app.route("/logout")
def logout():
    if isLoggedIn():
        session.pop("email", default=None)
    return redirect(url_for("login"))
