function submitLoginForm(formElement, url) {
    formElement.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Serialize form data into JSON
        var formData = {
            'username': formElement.querySelector('#username').value,
            'password': formElement.querySelector('#password').value
        };
    
        // Send form data as JSON via AJAX
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                window.location.href = 'dashboard'; // Redirect to protected page on success
            } else {
                return response.json().then(data => {
                    alert(data.error); // Display error message on failure
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}
