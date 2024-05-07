let modalNewAlbum = document.querySelector('.modal__new-album-container');

document.querySelector(".open-modal__new-album").addEventListener("click", () => {
    modalNewAlbum.style.display = "block";
})
document.querySelector(".close-modal__new-album").addEventListener("click", () => {
    modalNewAlbum.style.display = "none";
})