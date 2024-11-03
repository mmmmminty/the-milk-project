window.addEventListener('load', async () => {
  const url = window.location.href;
  const milk_id = url.split('/').pop();

  console.log(milk_id);
  const response = await fetch(`http://localhost:5010/milk?id=${milk_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Listener of Edit button
  document.getElementById('edit').addEventListener('click', () => {
    window.location.href = 'log-milk-nurse.html';
  });

  const milkInfo = await response.json();

  document.getElementById('milk').textContent = "Milk's Code #" + milkInfo.id;
  document.querySelector('.express-time').textContent = "Express Date: " + milkInfo.expressed;
  document.querySelector('.storing-type').textContent = "Storing Type: " + 
    (milkInfo.frozen ? "Frozen" : "Fridge") + 
    (milkInfo.defrosted ? " (defrosted)" : " (chilled)");
  document.querySelector('.expiry-time').textContent = "Expiry Date: " + milkInfo.expiry;
  document.querySelector('.batch-num').textContent = "Batch Number: " + (milkInfo.batch ? milkInfo.batch : "N/A");
  document.querySelector('.verified').textContent = "Status: " + (milkInfo.verified_id ? "Verified" : "Not Verified");
  document.querySelector('.volume').textContent = "Volume: " + milkInfo.volume + " ml";

  const nutrientsList = document.querySelector('.nutrients-list');
  const nutrients = milkInfo.additives;
  for (let nutrient in nutrients) {
    const listItem = document.createElement('li');
    listItem.textContent = nutrient;
    nutrientsList.appendChild(listItem);
    console.log(nutrient);
  };

});
