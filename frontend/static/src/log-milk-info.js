// // Listener of Edit button
// document.getElementById('edit').addEventListener('click', () => {
// 	window.location.href = 'log-milk-nurse.html';
// });

// // Provide milk info
// const response = await fetch(`http://localhost:${BACKEND_PORT}/milk?id=${milkId}`, {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: {},
//   });

// const milkInfo = await response.json();

// document.getElementById('milk').textContent = "Milk's Code #" + milkInfo.id
// document.querySelector('.baby-name').textContent = "Baby's Full Name: ";
// document.querySelector('.express-date').textContent = "Express Date: " + milkInfo.expressed;
// document.querySelector('.storing-type').textContent = "Storing Type: " + 
//     (milkInfo.frozen ? "Frozen" : "Fridge") + 
//     (milkInfo.defrosted ? " (defrosted)" : " (chilled)");
// document.querySelector('.expiry-date').textContent = "Expiry Date: " + milkInfo.expiry;

// const nutrientsList = document.querySelector('.nutrients-list');
// const nutrients = milkInfo.Additives;
// nutrients.forEach(nutrient => {
//     const listItem = document.createElement('li');
//     listItem.textContent = nutrient;
//     nutrientsList.appendChild(listItem);
// });
// Function to fetch and display milk info
async function fetchMilkInfo(milkId) {
  try {
      // Provide milk info
      const response = await fetch(`http://127.0.0.1:5010/milk?id=${milkId}`, {
          method: "GET",
          headers: {
              "Content-Type": "application/json",
          },
      });

      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }

      const milkInfo = await response.json();

      console.log(milkInfo)
      // Update the DOM with milk information
      document.getElementById('milk').textContent = "Milk's Code #" + milkInfo.id;
      document.querySelector('.baby-name').textContent = "Baby's Full Name: "; // You may want to add the baby's name here
      document.querySelector('.express-date').textContent = "Express Date: " + milkInfo.expressed;
      document.querySelector('.storing-type').textContent = "Storing Type: " +
          (milkInfo.frozen ? "Frozen" : "Fridge") +
          (milkInfo.defrosted ? " (defrosted)" : " (chilled)");
      document.querySelector('.expiry-date').textContent = "Expiry Date: " + milkInfo.expiry;

      const nutrientsList = document.querySelector('.nutrients-list');
      const nutrients = milkInfo.Additives || []; // Handle the case where Additives might not be present
      nutrients.forEach(nutrient => {
          const listItem = document.createElement('li');
          listItem.textContent = nutrient;
          nutrientsList.appendChild(listItem);
      });
  } catch (error) {
      console.error("Error fetching milk info:", error);
  }
}

// Call the function with the appropriate milkId
const milkId = '011694bf-7434-4aa8-a65e-349551c583fc'; // Replace with the actual milk ID you want to fetch
fetchMilkInfo(milkId);
