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
            
            // Set storage type
            const storageType = milkInfo.frozen ? 'freezer' : 'fridge';
            document.querySelector(`input[name="storage"][value="${storageType}"]`).checked = true;
            
            // Set expiry time
            const expiryTime = new Date(milkInfo.expiry);
            document.getElementById('expiryTime').value = expiryTime.toISOString().slice(0, 16);
            
            // Populate nutrients list
            const nutrientsList = document.getElementById('nutrientsList');
            if (milkInfo.additives) {
                milkInfo.additives.forEach(nutrient => {
                    const listItem = document.createElement('div');
                    listItem.className = 'nutrient-item';
                    
                    const bullet = document.createElement('span');
                    bullet.className = 'bullet';
                    bullet.textContent = '•';
                    
                    const text = document.createElement('span');
                    text.textContent = ` ${nutrient}`;
                    
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'delete-btn';
                    deleteBtn.innerHTML = '🗑️';
                    deleteBtn.onclick = () => listItem.remove();
                    
                    listItem.appendChild(bullet);
                    listItem.appendChild(text);
                    listItem.appendChild(deleteBtn);
                    nutrientsList.appendChild(listItem);
                });
            }
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
                const storage = document.querySelector('input[name="storage"]:checked').value;
                const expiryTime = document.getElementById('expiryTime').value;
                
                // Gather nutrients
                const nutrients = [];
                document.querySelectorAll('.nutrient-item span:not(.bullet)').forEach(span => {
                    nutrients.push(span.textContent.trim());
                });

                // Prepare payload
                const payload = {
                    expressed: new Date(expressTime).toISOString(),
                    frozen: storage === 'freezer',
                    expiry: new Date(expiryTime).toISOString()
                };

                if (milkId) {
                    payload.id = milkId;
                }

                // Save main milk data
                const url = `http://localhost:${BACKEND_PORT}/milk`;
                const result = milkId 
                    ? await put(url, payload)
                    : await post(url, payload);

                const savedMilkId = result.milk_id || milkId;

                // Save nutrients
                for (const nutrient of nutrients) {
                    const [amount, ...nameParts] = nutrient.split(' ');
                    const additivePayload = {
                        additive: nameParts.join(' '),
                        amount: parseFloat(amount),
                        milkId: savedMilkId
                    };

                    await post(`http://localhost:${BACKEND_PORT}/milk/additive`, additivePayload);
                }

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

// Keep existing getDateTime function
function getDateTime() {
    const now = new Date();
    const currentDateTime = now.toISOString().slice(0, 16);
    
    // Set express time
    const expressInput = document.getElementById('expressTime');
    if (expressInput && !expressInput.value) {
        expressInput.value = currentDateTime;
    }

    // Calculate and set expiry time
    updateExpiryTime();
}

// Update expiry time based on storage type
function updateExpiryTime() {
    const expressTime = new Date(document.getElementById('expressTime').value);
    const storageType = document.querySelector('input[name="storage"]:checked').value;
    const expiryInput = document.getElementById('expiryTime');
    
    if (storageType === 'fridge') {
        const fridgeExpiry = new Date(expressTime);
        fridgeExpiry.setDate(fridgeExpiry.getDate() + 4);
        expiryInput.value = fridgeExpiry.toISOString().slice(0, 16);
    } else {
        const freezerExpiry = new Date(expressTime);
        freezerExpiry.setMonth(freezerExpiry.getMonth() + 6);
        expiryInput.value = freezerExpiry.toISOString().slice(0, 16);
    }
}

// Keep existing addNutrient function with modifications
function addNutrient() {
    const name = document.getElementById('nutrientName').value.trim();
    const value = document.getElementById('nutrientValue').value;
    const unit = document.getElementById('nutrientUnit').value;
    
    if (name && value) {
        const list = document.getElementById('nutrientsList');
        const item = document.createElement('div');
        item.className = 'nutrient-item';
        
        const bullet = document.createElement('span');
        bullet.className = 'bullet';
        bullet.textContent = '•';
        
        const text = document.createElement('span');
        text.textContent = ` ${value}${unit} ${name}`;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.onclick = function() {
            item.remove();
        };
        
        item.appendChild(bullet);
        item.appendChild(text);
        item.appendChild(deleteBtn);
        list.appendChild(item);
        
        // Clear inputs
        document.getElementById('nutrientName').value = '';
        document.getElementById('nutrientValue').value = '';
    }
}

// Add event listeners for storage type change
document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="storage"]');
    radioButtons.forEach(button => {
        button.addEventListener('change', updateExpiryTime);
    });
    
    // Add event listeners for nutrient input
    const nutrientName = document.getElementById('nutrientName');
    const nutrientValue = document.getElementById('nutrientValue');
    const addButton = document.querySelector('.nutrient-add-group button');
    
    if (addButton) {
        addButton.addEventListener('click', addNutrient);
    }
    
    if (nutrientName && nutrientValue) {
        [nutrientName, nutrientValue].forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    addNutrient();
                }
            });
        });
    }
});