// Listener of Back button
document.getElementById('back-match').addEventListener('click', () => {
	window.location.href = 'scanner.html';
});

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