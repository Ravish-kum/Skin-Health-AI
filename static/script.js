document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput) return; // Only run on pages that have fileInput

    const uploadBox = document.getElementById("uploadBox");
    const previewImage = document.getElementById("previewImage");
    const uploadContent = document.getElementById("uploadContent");
    const clearBtn = document.getElementById("clearBtn");

    // Click to open file dialog
    uploadBox.addEventListener("click", () => {
        fileInput.click();
    });

    // When file selected
    fileInput.addEventListener("change", handleFile);

    // Drag over
    uploadBox.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = "orange"; 
    });

    // Drag leave
    uploadBox.addEventListener("dragleave", () => {
        uploadBox.style.borderColor = "#555";
    });

    // Drop
    uploadBox.addEventListener("drop", (e) => {
        e.preventDefault();
        fileInput.files = e.dataTransfer.files;
        handleFile();
    });

    // Handle preview
    function handleFile() {
        const file = fileInput.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
            uploadContent.style.display = "none";
        }
        reader.readAsDataURL(file);
    }

    // Clear button
    clearBtn.addEventListener("click", (e) => {
        e.stopPropagation(); // Prevent clicking the clear button from triggering uploadBox click
        fileInput.value = "";
        previewImage.src = "";
        previewImage.style.display = "none";
        uploadContent.style.display = "block";
    });
});
