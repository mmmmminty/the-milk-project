import { BACKEND_PORT } from './config.js';
import { getMilk, post, put } from './api.js';

document.addEventListener('DOMContentLoaded', async function() {
    const urlParams = new URLSearchParams(window.location.search);
    const milkId = urlParams.get('id');
    
    // Initialize the date/time fields
    getDateTime();

    // If we have a milk ID, fetch and populate the data
    if (milkId) {
        try {
            const milkInfo = await getMilk(milkId);
            
            // Update title
            document.querySelector('h1').textContent = `Milk #${milkInfo.id}`;
            
            // Update baby name text
            document.querySelector('.baby-name').textContent = `Baby's Full Name: ${milkInfo.babyName || ''}`;
            
            // Set express time
            const expressTime = new Date(milkInfo.expressed);
            document.getElementById('expressTime').value = expressTime.toISOString().slice(0, 16);
            
        } catch (error) {
            console.error("Error fetching milk info:", error);
        }
    }

    // Add save button functionality
    const saveButton = document.querySelector('.log-milk button:last-child');
    if (saveButton) {
        saveButton.addEventListener('click', async function() {
            try {
                const expressTime = document.getElementById('expressTime').value;
                
                // Prepare payload
                const payload = {
                    expressed: new Date(expressTime).toISOString(),
                    // Default to fridge storage for mother's entries
                    frozen: false
                };

                if (milkId) {
                    payload.id = milkId;
                }

                // Save milk data
                const url = `http://localhost:${BACKEND_PORT}/milk`;
                const result = milkId 
                    ? await put(url, payload)
                    : await post(url, payload);

                const savedMilkId = result.milk_id || milkId;

                // If this was a new entry, redirect to the saved entry
                if (!milkId) {
                    window.location.href = `?id=${savedMilkId}`;
                } else {
                    alert('Saved successfully!');
                }

            } catch (error) {
                console.error("Error saving milk info:", error);
            }
        });
    }
});

// Function to set current date/time
function getDateTime() {
    const now = new Date();
    const currentDateTime = now.toISOString().slice(0, 16);
    
    // Set express time
    const expressInput = document.getElementById('expressTime');
    if (expressInput && !expressInput.value) {
        expressInput.value = currentDateTime;
    }
}

// Initialize date/time input when clicking
document.addEventListener('DOMContentLoaded', function() {
    const timeInput = document.getElementById('expressTime');
    if (timeInput) {
        timeInput.addEventListener('click', function() {
            if (!this.value) {
                getDateTime();
            }
        });
    }
});