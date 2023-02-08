
const fileInput = document.querySelector('#file-profile-pic input[type=file]');
fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
        const fileName = document.querySelector('#file-profile-pic .file-name');
        fileName.textContent = fileInput.files[0].name;
    }
}
