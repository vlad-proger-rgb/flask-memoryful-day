let modalWriteDay = document.querySelector('.modal__write-day-container');
let writeDayForm = document.getElementById("write-day-form");

document.querySelector(".open-modal__write-day").addEventListener("click", () => {
    modalWriteDay.style.display = "block";
})
document.querySelector(".close-modal__write-day").addEventListener("click", () => {
    modalWriteDay.style.display = "none";
})

function saveDay() {
    const formData = new FormData(writeDayForm);
    const actionUrl = writeDayForm.action;
    formData["description"] = formData.get("description").trim();
    fetch(actionUrl, {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            throw new Error('Error saving day');
        }
        location.reload();
    }).catch(error => {
        alert('Error saving day: ' + error);
    });
}