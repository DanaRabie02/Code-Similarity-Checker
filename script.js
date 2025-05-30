<<<<<<< HEAD
async function generateResult() {
    const code1 = document.getElementById('code1').value.trim();
    const code2 = document.getElementById('code2').value.trim();
    const resultDiv = document.getElementById('result');

    // Validate input
    if (!code1 || !code2) {
        resultDiv.innerHTML = '<p class="error">Please enter both Code 1 and Code 2.</p>';
        return;
    }

    // Show loading state
    resultDiv.innerHTML = '<p>Analyzing…</p>';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code1, code2 })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        resultDiv.innerHTML = `<p>Detected clone type: <strong>${data.type}</strong></p>`;
    } catch (err) {
        console.error('Error calling backend:', err);
        resultDiv.innerHTML = '<p class="error">Error connecting to the server. Please make sure the backend is running.</p>';
    }
}
=======
async function generateResult() {
    const code1 = document.getElementById('code1').value.trim();
    const code2 = document.getElementById('code2').value.trim();
    const resultDiv = document.getElementById('result');

    // Validate input
    if (!code1 || !code2) {
        resultDiv.innerHTML = '<p class="error">Please enter both Code 1 and Code 2.</p>';
        return;
    }

    // Show loading state
    resultDiv.innerHTML = '<p>Analyzing…</p>';

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code1, code2 })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        resultDiv.innerHTML = `<p>Detected clone type: <strong>${data.type}</strong></p>`;
    } catch (err) {
        console.error('Error calling backend:', err);
        resultDiv.innerHTML = '<p class="error">Error connecting to the server. Please make sure the backend is running.</p>';
    }
}
>>>>>>> ce8be2b424992ac19685c1e303784871c4a85789
