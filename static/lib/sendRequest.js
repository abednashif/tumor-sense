    function sendRequest(route) {
        fetch(route, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({data: 'example'}),
        })
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }