// Add any interactive JavaScript functionality here if needed
document.getElementById('diagnosis-form').addEventListener('submit', function (e) {
    const fileInput = document.getElementById('image');
    const queryInput = document.getElementById('query');

    if (!fileInput.files.length || !queryInput.value.trim()) {
        e.preventDefault();
        alert('Please upload an image and describe your symptoms.');
    }
});