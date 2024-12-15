document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const productGrid = document.querySelector('.product-grid');
    const filterForm = document.querySelector('.filter-form');

    // Event listener for keyup on search bar
    searchBar.addEventListener('keyup', async () => {
        const formData = new FormData(filterForm); // Gather form data
        const queryString = new URLSearchParams(formData).toString(); // Convert to query string

        try {
            const response = await fetch(`${filterForm.action}?${queryString}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newProductGrid = doc.querySelector('.product-grid');
                productGrid.innerHTML = newProductGrid.innerHTML; // Update the product grid
            } else {
                console.error('Failed to fetch products:', response.status);
            }
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    });
});


console.log("Hello world!");

document.addEventListener('DOMContentLoaded', function () {
    if (typeof flashed_messages !== 'undefined' && flashed_messages.length > 0) {
        flashed_messages.forEach(message => {
            const [category, text] = message; // Extract category and message text
            toastr.options = {
                "closeButton": true,
                "progressBar": true,
                "positionClass": "toast-top-right custom-toast-top", // Added custom class
                "timeOut": "5000",
            };
            toastr[category](text); // Show the notification
        });
    }
});








