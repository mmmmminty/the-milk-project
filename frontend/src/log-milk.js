function getDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; // January is 0!
    var yyyy = today.getFullYear();
    var hh = today.getHours();
    var min = today.getMinutes();
  
    // Add leading zeros where needed
    if (dd < 10) {
        dd = '0' + dd;
    } 
  
    if (mm < 10) {
        mm = '0' + mm;
    }

    if (hh < 10) {
        hh = '0' + hh;
    }

    if (min < 10) {
        min = '0' + min;
    }
  
    // Format for datetime-local input (YYYY-MM-DDThh:mm)
    var dateTime = `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    console.log(dateTime);
    document.getElementById("expressTime").value = dateTime;
}
  
window.onload = function() {
    getDate();
};