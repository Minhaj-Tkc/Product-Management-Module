// Automatically submit the form on quantity change
document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', (event) => {
        const url = event.target.dataset.url;
        const quantity = event.target.value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                quantity: quantity
            })
        }).then(response => {
            if (response.ok) {
                location.reload(); // Reload the page to reflect updated values
            } else {
                alert('Failed to update the cart.');
            }
        });
    });
});