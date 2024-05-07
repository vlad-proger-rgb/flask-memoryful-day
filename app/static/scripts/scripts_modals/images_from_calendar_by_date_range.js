
let modalImagesFromCalendar = document.querySelector('.modal__images-from-calendar-by-date-range-container');
document.querySelector('.open-modal__images-from-calendar-by-date-range').addEventListener('click', () => {
    modalImagesFromCalendar.style.display = 'block';
})

document.querySelector(".close-modal__images-from-calendar-by-date-range").addEventListener("click", () => {
    modalImagesFromCalendar.style.display = 'none';
})

function findImagesFromCalendarByDateRange() {
    let existingImagesContainer = document.querySelector('.modal__images-from-calendar-by-date-range-container > .modal-content > .modal-body > div');
    let formData = new FormData();
    formData.append('start_date', startDate.value);
    formData.append('end_date', endDate.value);

    fetch('/gallery/images_by_date_range', {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            console.log(response);
            alert('Error finding images:', response);
            throw new Error('Error finding images');
        }
        console.log("response:", response);
        return response.text();
    }).then(data => {
        console.log("data:", data);
        existingImagesContainer.innerHTML = data;

        document.querySelectorAll(".existing-image").forEach(image => {
            console.log("some")
            image.addEventListener('click', () => {
                image.classList.toggle('selected');
            })
        })
    }).catch(error => {
        alert('Error finding images: ' + error);
    });
}


function addImagesToAlbumFromCalendar(albumName) {
    let selectedImages = Array.from(document.querySelectorAll('.existing-image.selected')).map(image => image.id);
    console.log("addImagesToAlbumFromCalendar() => selectedImages:", selectedImages);

    let formData = new FormData();
    formData.append('images_to_add', selectedImages);

    if (selectedImages.length === 0) {
        alert("Please select at least one image to add to the album. Or close the modal.");
        return;
    }

    if (!albumName) {
        alert("Ok! These images will be added to the album that you're creating");
        modalImagesFromCalendar.style.display = "none";
        return
    }

    fetch(`/gallery/album/${albumName}/add_images_from_calendar`, {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            console.log(response);
            alert('Error adding images:', response);
            throw new Error('Error adding images');
        }
        console.log("response:", response);
        return response.json();
    }).then(data => {
        console.log("data:", data);
        alert(data.message);
        modalImagesFromCalendar.style.display = "none";
        location.reload();
    }).catch(error => {
        alert('Error adding images: ' + error);
    });
}