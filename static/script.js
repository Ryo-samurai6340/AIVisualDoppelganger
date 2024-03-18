function showContent() {
    setTimeout(function() {
        document.getElementById('preloader').style.display = 'none';
        document.getElementById('body_content').style.display = 'block';
    }, 3000);
}
// Event listener to call showContent function when the page is fully loaded
window.addEventListener('load', showContent);

// Function to validate image upload
function validateImage() {
    let image = document.getElementById("image").files[0]; // Get uploaded image file
    if (!image) {
        // Display error message if no image is uploaded
        alert("Please upload an image.");
        return false; // Return false if no image is uploaded
    }
    return true; // Return true if image is uploaded
}

// Function to show the loading spinner
function showLoadingSpinner() {
    if(!validateImage()) {
        return; 
    }
    document.getElementById('loadingSpinner').style.display = 'block';
}

// Function to hide the loading spinner
function hideLoadingSpinner() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

// Function to enable/disable download button based on image availability
function toggleDownloadButton(enabled) {
    var downloadButton = document.getElementById('downloadButton');
    downloadButton.disabled = !enabled;
}

// updateImages function to update image & enable to download the replicated img
function updateImages(originalImageData, replicatedImageData) {
    var originalImage = document.getElementById('originalImage');
    var replicatedImage = document.getElementById('replicatedImage');

    originalImage.src = "data:image/png;base64," + originalImageData;
    replicatedImage.src = "data:image/png;base64," + replicatedImageData;

    hideLoadingSpinner(); // Hide the loading spinner after updating images

    // Enable download button if both images are available
    toggleDownloadButton(originalImageData && replicatedImageData);
}

function downloadReplicatedImage() {
    var replicatedImage = document.getElementById('replicatedImage');
    var link = document.createElement('a');
    link.href = replicatedImage.src;
    link.download = 'replicated_image.png';
    link.click();
}

// Function to enable users to send message from the contact section
function sendMail() {
    event.preventDefault(); 
    // Validate the form before sending the email
    if (!validateForm()) {
        return; // Exit the function if form validation fails
    }
    
    let parms = {
        from_name : document.getElementById("name").value,
        email : document.getElementById("email").value,
        subject : document.getElementById("subject").value, 
        message : document.getElementById("message").value,
    }
    emailjs.send("service_txmsajv", "template_li27qnr", parms).then(function() {
        displayStatusMessage("Your enquiry has been sent successfully!", true);
        setTimeout(function() {
            window.location.reload();
        }, 3000); 
    }, function(error) {
        console.error('Failed to send email:', error);
        displayStatusMessage("Failed to send email. Please try again later.", false);
    });
}

function displayStatusMessage(message, success) {
    let statusMessageElement = document.getElementById("status-message");
    statusMessageElement.textContent = message;
    statusMessageElement.style.color = success ? "green" : "red";
}

// Function to validate input fields
function validateForm() {
    // Get values of input fields
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let subject = document.getElementById("subject").value;
    let message = document.getElementById("message").value;

    // Check if any input field is empty
    if (name === "" || email === "" || subject === "" || message === "") {
        // Display error message
        displayStatusMessage("Please fill in all fields.", false);
        return false; // Return false to prevent form submission
    }
    return true; // Return true if all fields are filled
}
document.getElementById("contact-form").addEventListener("submit", sendMail);

// To show scrollup 
const scrollUp = () => {
    const scrollUp = document.getElementById('scroll-up');

    // When the scroll is higher than 350 viewport height, add the show-scroll class to teh a tag with the scrollup
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
                        : scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp);
