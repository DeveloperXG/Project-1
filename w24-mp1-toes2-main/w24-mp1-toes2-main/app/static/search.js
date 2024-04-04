const borrowButtons = document.querySelectorAll(".borrow-btn");

borrowButtons.forEach(button => {
	button.addEventListener("click", (event) => {
		if (!button.classList.contains("disabled-btn")) {
			let id = event.target.dataset.id;

			let formData = new FormData()
			formData.append("book_id", id)

			fetch("/return", {
				method: "post",
				body: formData
			});
			button.classList.add("disabled-btn")
		}
	});
});