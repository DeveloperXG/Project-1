from collections import namedtuple

Profile = namedtuple(
    "Profile", "member, borrowCounts, unpaidPenaltyCount, totalDebt")
