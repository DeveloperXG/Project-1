// global variables
let borrowId;
const popupForm = document.getElementById('popup-form-page');

// show popup on click of return button
const returnButtons = document.querySelectorAll('.return-btn');
returnButtons.forEach(button => {
	button.addEventListener('click', function (event) {
		// get returnID
		borrowId = event.target.parentElement.firstElementChild.dataset.bid;
		popupForm.style.display = 'flex';
	});
});

// show prompt on click of penalty button

// when cancel button is clicked
document.getElementById('cancel-btn').addEventListener('click', function (event) {
	event.preventDefault();

	// clear form
	popupForm.style.display = 'none';
	const formElement = event.target.parentElement;

	let formData = new FormData();
	formData.append('bid', borrowId);
	//give serve bid and ask it to return that book
	fetch(formElement.getAttribute('action'), {
		method: formElement.getAttribute('method'),
		body: formData
	}).then((_) => {
		location.reload(); // refresh page with new page removed the returned borrowing
	});
});

// submit return data and refresh page
document.getElementById('return-form').addEventListener('submit', function (event) {
	event.preventDefault();

	let formData = new FormData(this);
	formData.append('bid', borrowId); // send the id of the borrowing that got returned
	event.target.parentElement.style.display = 'none';

	fetch(this.getAttribute('action'), {
		method: this.getAttribute('method'),
		body: formData
	}).then((_) => {
		location.reload(); // refresh page with new page removed the returned borrowing
	});
});