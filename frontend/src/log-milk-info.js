// Listener of Edit button
document.getElementById('edit').addEventListener('click', () => {
	window.location.href = 'log-milk-nurse.html';
});

// Provide milk info
const response = await fetch(`http://localhost:${BACKEND_PORT}/milk?id=${milkId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: {},
  });

const milkInfo = await response.json();

document.getElementById('milk').textContent = "Milk's Code #" + milkInfo.id
document.querySelector('.baby-name').textContent = "Baby's Full Name: ";
document.querySelector('.express-date').textContent = "Express Date: " + milkInfo.expressed;
document.querySelector('.storing-type').textContent = "Storing Type: " + 
    (milkInfo.frozen ? "Frozen" : "Fridge") + 
    (milkInfo.defrosted ? " (defrosted)" : " (chilled)");
document.querySelector('.expiry-date').textContent = "Expiry Date: " + milkInfo.expiry;

const nutrientsList = document.querySelector('.nutrients-list');
const nutrients = milkInfo.Additives;
nutrients.forEach(nutrient => {
    const listItem = document.createElement('li');
    listItem.textContent = nutrient;
    nutrientsList.appendChild(listItem);
});
