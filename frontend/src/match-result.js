// Listener of Back button
document.getElementById('back-match').addEventListener('click', () => {
	window.location.href = 'scanner.html';
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

// Provide Patient info
// const response_patient = await fetch(`http://localhost:${BACKEND_PORT}/patient?id=${patientId}`, {
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: {},
//   });

// const patientInfo = await response.json();
// document.getElementById('patient').textContent = "Patient's Code #" + patientId;
// document.querySelector('.patient-name').textContent = "Patient's Full Name: " + patientInfo.name;
// document.querySelector('.gender').textContent = "Gender: " + patientInfo.gender;
// document.querySelector('.dob').textContent = "Date of Birth: " + patientInfo.dob;
// document.querySelector('.status').textContent = "Status: " + (patientInfo.status ? "Baby" : "Mom");

