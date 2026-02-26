const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const uploadText = document.getElementById("uploadText");
const predictionBox = document.getElementById("predictionBox");

let selectedFile = null;

fileInput.addEventListener("change", function () {
  selectedFile = this.files[0];

  if (selectedFile) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      previewImage.style.display = "block";
      uploadText.style.display = "none";
    };
    reader.readAsDataURL(selectedFile);
  }
});

// function predict() {
//   if (!selectedFile) {
//     alert("Please upload an image first.");
//     return;
//   }

//   predictionBox.innerHTML = "Predicting...";

//   // ⚠️ Replace this with real API call later
//   // Example simulation:
//   setTimeout(() => {
//     const fakePrediction = "Eczema";
//     const fakeConfidence = 0.927;

//     predictionBox.innerHTML = `
//       <strong>${fakePrediction}</strong>
//       <br>
//       Confidence: ${fakeConfidence}
//     `;
//   }, 1500);
// }

function clearAll() {
  selectedFile = null;
  fileInput.value = "";
  previewImage.style.display = "none";
  uploadText.style.display = "block";
  predictionBox.innerHTML = "Waiting for prediction...";
}

