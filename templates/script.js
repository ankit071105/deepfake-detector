// File preview functionality
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const preview = document.getElementById('preview');
    const videoPreview = document.getElementById('videoPreview');
    
    if (file.type.match('video.*')) {
        const videoURL = URL.createObjectURL(file);
        videoPreview.src = videoURL;
        preview.classList.remove('d-none');
    } else {
        preview.classList.add('d-none');
        alert('Please select a video file');
    }
});

// Form submission handling
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        e.preventDefault();
        alert('Please select a file first');
    } else {
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
    }
});