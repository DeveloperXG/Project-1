// global variables
const popupForm = document.getElementById('popup-form-page');
let penaltyID;

// show popup on click of return button
const returnButtons = document.querySelectorAll('.penalty-btn');
returnButtons.forEach(button => {
	button.addEventListener('click', function (event) {
		// get returnID
		penaltyID = event.target.parentElement.dataset.pid;
		let amountLeft = event.target.parentElement.dataset.balance;

		let amountInput = document.getElementById('payment');
		amountInput.setAttribute('max', amountLeft);
		amountInput.setAttribute('value', amountLeft);

		popupForm.style.display = 'flex';
	});
});

// show prompt on click of penalty button

// when cancel button is clicked clear form and remove popup
document.getElementById('cancel-btn').addEventListener('click', function (event) {
	popupForm.style.display = 'none';
});

// submit return data and refresh page
document.getElementById('return-form').addEventListener('submit', function (event) {
	event.preventDefault();

	let formData = new FormData(this);
	formData.append('pid', penaltyID); // send the id of the borrowing that got returned

	fetch("/penalty", {
		method: "post",
		body: formData
	}).then((_) => {
		location.reload(); // refresh page
	});
});