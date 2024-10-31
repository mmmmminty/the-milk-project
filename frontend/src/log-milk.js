document.addEventListener('DOMContentLoaded', function() {
    getDateTime();
});

function getDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');

    const currentDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
    
    // Set express time
    const expressInput = document.getElementById('expressTime');
    if (expressInput) {
        expressInput.value = currentDateTime;
    }

    // Calculate and set expiry time (4 days later for fridge, 6 months for freezer)
    const expiryInput = document.getElementById('expiryTime');
    if (expiryInput) {
        // Default to fridge expiry (4 days)
        const expiry = new Date(now);
        expiry.setDate(expiry.getDate() + 4);
        
        const expiryYear = expiry.getFullYear();
        const expiryMonth = String(expiry.getMonth() + 1).padStart(2, '0');
        const expiryDay = String(expiry.getDate()).padStart(2, '0');
        const expiryHours = String(expiry.getHours()).padStart(2, '0');
        const expiryMinutes = String(expiry.getMinutes()).padStart(2, '0');
        
        expiryInput.value = `${expiryYear}-${expiryMonth}-${expiryDay}T${expiryHours}:${expiryMinutes}`;
    }
}

// Update expiry time when storage type changes
document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="storage"]');
    radioButtons.forEach(button => {
        button.addEventListener('change', function() {
            const expressTime = new Date(document.getElementById('expressTime').value);
            const expiryInput = document.getElementById('expiryTime');
            
            if (this.value === 'fridge') {
                const fridgeExpiry = new Date(expressTime);
                fridgeExpiry.setDate(fridgeExpiry.getDate() + 4);
                expiryInput.value = fridgeExpiry.toISOString().slice(0, 16);
            } else if (this.value === 'freezer') {
                const freezerExpiry = new Date(expressTime);
                freezerExpiry.setMonth(freezerExpiry.getMonth() + 6);
                expiryInput.value = freezerExpiry.toISOString().slice(0, 16);
            }
        });
    });
});

// Nutrient list functionality
function addNutrient() {
    const name = document.getElementById('nutrientName').value.trim();
    const value = document.getElementById('nutrientValue').value;
    const unit = document.getElementById('nutrientUnit').value;
    
    if (name && value) {
        const list = document.getElementById('nutrientsList');
        const item = document.createElement('div');
        item.className = 'nutrient-item';
        
        // Create bullet point span
        const bullet = document.createElement('span');
        bullet.className = 'bullet';
        bullet.textContent = '•';
        
        // Create text content span
        const text = document.createElement('span');
        text.textContent = ` ${value}${unit} ${name}`;
        
        // Create delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.onclick = function() {
            item.remove();
        };
        
        // Assemble the item
        item.appendChild(bullet);
        item.appendChild(text);
        item.appendChild(deleteBtn);
        
        // Add to list
        list.appendChild(item);
        
        // Clear inputs
        document.getElementById('nutrientName').value = '';
        document.getElementById('nutrientValue').value = '';
    }
}

// Initialize event listeners when page loads
window.onload = function() {
    getDateTime();
    
    // Add click handler for datetime input
    const timeInput = document.getElementById('expressTime');
    if (timeInput) {
        timeInput.addEventListener('click', function() {
            getDateTime();
        });
    }
    
    // Add enter key handler for nutrient inputs
    const nutrientName = document.getElementById('nutrientName');
    const nutrientValue = document.getElementById('nutrientValue');
    
    if (nutrientName && nutrientValue) {
        [nutrientName, nutrientValue].forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    addNutrient();
                }
            });
        });
    }
};