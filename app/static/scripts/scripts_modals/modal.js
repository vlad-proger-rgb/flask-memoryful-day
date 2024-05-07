document.querySelectorAll(".modal").forEach(function(modal) {
    modal.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});