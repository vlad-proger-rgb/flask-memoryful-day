document.addEventListener("click", function(event) {
    let targetElement = event.target;
    if (targetElement.classList.contains("fullscreenable")) {
        let fullscreenImage = document.querySelector(".fullscreen-image");
        fullscreenImage.src = targetElement.src;

        let fullscreenImageContainer = document.querySelector(".fullscreen-image-container");
        fullscreenImageContainer.style.display = "block";
    }
});

document.addEventListener("click", function(event) {
    let targetElement = event.target;
    if (targetElement.classList.contains("fullscreen-image-container") ||
        targetElement.classList.contains("close-button")
    ) {
        let fullscreenImageContainer = document.querySelector(".fullscreen-image-container");
        fullscreenImageContainer.style.display = "none";
    }
});