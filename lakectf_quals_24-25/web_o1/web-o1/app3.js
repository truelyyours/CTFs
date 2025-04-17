const express = require('express');
const app = express();

// Use built-in JSON middleware
app.use(express.json());

// POST /proxy endpoint
app.post('/proxy', async (req, res) => {
    const url = req.body.url;
    if (!url) {
        return res.status(400).send('Missing url parameter');
    }

    try {
        // Use Node.js's built-in fetch function
        const response = await fetch(url);
        const data = await response.text();

        // Forward the response back to the caller
        res.status(response.status).send(data);
    } catch (error) {
        console.error('Error fetching the URL:', error);
        res.status(500).send('Error fetching the URL');
    }
});

// Start the Express server on port 3000
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Third proxy running on port ${PORT}`);
});
