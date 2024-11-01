// Listener of Back button
document.getElementById('back-match').addEventListener('click', () => {
	window.location.href = 'scanner.html';
});

// Provide milk info
apiCall(`milk?id=${milkId}`, 'GET', {}, token).then(milkInfo => {
    document.querySelector('.baby-name').textContent = "Baby's Full Name: ";
    document.querySelector('.express-date').textContent = "Express Date: " + milkInfo.Expressed;
    document.querySelector('.storing-type').textContent = "Storing Type: " + 
        (milkInfo.Frozen ? "Frozen" : "Fridge") + 
        (milk.Defrosted ? " (defrosted)" : " (chilled)");
    document.querySelector('.expiry-date').textContent = "Expiry Date: " + milkInfo.Expiry;

    const nutrientsList = document.querySelector('.nutrients-list');
    const nutrients = milkInfo.Additives;
    nutrients.forEach(nutrient => {
        const listItem = document.createElement('li');
        listItem.textContent = nutrient;
        nutrientsList.appendChild(listItem);
    });
})

// Provide patient info
apiCall(`milk?id=${milkId}`, 'GET', {}, token).then(milkInfo => {
    document.getElementById('milk').textContent = "Milk's Code #" + milkId;
    document.querySelector('.baby-name').textContent = "Baby's Full Name: ";
    document.querySelector('.express-date').textContent = "Express Date: " + milkInfo.Expressed;
    document.querySelector('.storing-type').textContent = "Storing Type: " + 
        (milkInfo.Frozen ? "Frozen" : "Fridge") + 
        (milk.Defrosted ? " (defrosted)" : " (chilled)");
    document.querySelector('.expiry-date').textContent = "Expiry Date: " + milkInfo.Expiry;

    const nutrientsList = document.querySelector('.nutrients-list');
    const nutrients = milkInfo.Additives;
    nutrients.forEach(nutrient => {
        const listItem = document.createElement('li');
        listItem.textContent = nutrient;
        nutrientsList.appendChild(listItem);
    });
})
