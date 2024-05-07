let modalImagesByURL = document.querySelector('.modal__images-by-url-container');
let imageByURLInputs = document.querySelector('.image-by-url-inputs');

document.querySelector('.open-modal__images-by-url').addEventListener('click', () => {
    modalImagesByURL.style.display = 'block';
})

document.querySelector(".close-modal__images-by-url").addEventListener("click", () => {
    modalImagesByURL.style.display = 'none';
})

function appendURLInput() {
    let newInput = document.createElement('div');
    newInput.classList.add('image-by-url__input');
    newInput.innerHTML = `
        <input class="image-by-url" type="url" name="urls" placeholder="https://example.com">
        <button class="left-right" onclick="removeURLInput(event)">X</button>
    `;
    imageByURLInputs.appendChild(newInput);
}


function removeURLInput(event) {
    event.target.parentElement.remove();
}


function addImagesByURLs(albumName) {
    let imageURLs = Array.from(document.querySelectorAll('.image-by-url')).map(image => image.value.trim());

    if (!imageURLs.length) {
        alert("Please, enter at least one URL.");
        return;
    }

    if (!albumName) {
        alert("Ok! These images by URLs will be added to the album that you're creating");
        modalImagesByURL.style.display = "none";
        return;
    }

    let formData = new FormData();

    formData.append("images_by_urls", imageURLs);

    fetch(`/gallery/album/${albumName}/add_images_by_urls`, {
        method: "POST",
        body: formData
    }).then(response => {
        if (!response.ok) {
            console.log(response);
            alert('Error adding image:', response);
            throw new Error('Error adding image');
        }
        location.reload();
    }).catch(error => {
        alert('Error adding image: ' + error);
    });
}