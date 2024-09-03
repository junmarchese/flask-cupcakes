$(document).ready(function() {
    
    // Function to generate HTML for a cupcake
    function generateCupcakeHTML(cupcake) {
        return `
            <li>
                <img src="${cupcake.image}" alt="${cupcake.flavor}" width="100">
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            </li>
        `;
    }

    // Function to fetch and display all cupcakes
    async function fetchAndDisplayCupcakes() {
        const response = await axios.get('/api/cupcakes');
        for (let cupcake of response.data.cupcakes) {
            $('#cupcake-list').append(generateCupcakeHTML(cupcake));
        }
    }

    // Handle form submission for adding a new cupcake and updates list on page to display it.
    $('#cupcake-form').on('submit', async function(evt) {
        evt.preventDefault();

        const flavor = $('#flavor').val();
        const size = $('#size').val();
        const rating = $('#rating').val();
        const image = $('#image').val();

        const response = await axios.post('/api/cupcakes', {
            flavor,
            size,
            rating,
            image
        });

        const newCupcake = response.data.cupcake;
        $('#cupcake-list').append(generateCupcakeHTML(newCupcake));

        //Clear the form
        $('#cupcake-form').trigger("reset");
    });

    //Initially fetch and display cupcakes
    fetchAndDisplayCupcakes();
});
