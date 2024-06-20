let modalNewAlbum = document.querySelector('.modal__new-album-container');
let startDate = document.querySelector('.start-date');
let endDate = document.querySelector('.end-date');


document.querySelector(".open-modal__new-album").addEventListener("click", () => {
    modalNewAlbum.style.display = "block";
})
document.querySelector(".close-modal__new-album").addEventListener("click", () => {
    modalNewAlbum.style.display = "none";
})

startDate.value = new Date(new Date() - 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0];
endDate.value = new Date().toISOString().split("T")[0];


function createAlbum() {
    let newAlbumName = document.querySelector('.new-album-name');
    let newAlbumImages = document.getElementById('new-album-images');

    let existingImagesIds = Array.from(document.querySelectorAll('.existing-image.selected')).map(image => image.id);
    let imagesURLs = Array.from(document.querySelectorAll('.image-by-url')).map(image => image.value.trim());

    if (!newAlbumName.value.trim()) {
        alert("Please, enter a valid album name. It can't be empty or contain only spaces.");
        return;
    }

    let albumNames = Array.from(document.querySelectorAll('.albom-item-square__name')).map(name => name.innerHTML);
    console.log(albumNames)

    for (name of albumNames) {
        if (name === newAlbumName.value) {
            alert("Album with this name already exists");
            return;
        }
    }


    console.log("newAlbumImages.files.length", newAlbumImages.files.length)
    console.log("existingImagesIds.length", existingImagesIds.length)
    console.log("imagesURLs.length", imagesURLs.length)
    console.log("imagesURLs:", imagesURLs)

    if (!newAlbumImages.files.length && !existingImagesIds.length & !imagesURLs.length) {
        alert("Please, select at least one image from your device or calendar or add images by URL");
        return;
    }

    let formData = new FormData();
    formData.append('name', newAlbumName.value);
    for (file of newAlbumImages.files) {
        formData.append('images[]', file);
    }
    formData.append('existing_images', existingImagesIds);
    formData.append('images_by_urls', imagesURLs);

    fetch('/gallery/new_album', {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            console.log(response);
            alert('Error creating album:', response);
            throw new Error('Error creating album');
        }
        console.log("response:", response);
        return response.json();
    }).then(data => {
        console.log("data:", data);
        location.reload();
    }).catch(error => {
        alert('Error creating album: ' + error);
    });
};