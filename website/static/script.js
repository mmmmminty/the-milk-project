// Milk Project website Javascript

/*
    Milk Project website Javascript
    By Kelly C (15/10/2024)
*/


document.getElementById("create_qr").addEventListener("click", function() {
    window.location.href = "/create";
});

let html5QrcodeScanner;
document.getElementById("scan_qr").addEventListener("click", function() {
    document.getElementById("result").clear;
    document.getElementById("reader").style.display = "block";
    if (!html5QrcodeScanner) {
        html5QrcodeScanner = new Html5QrcodeScanner(
            "reader", { fps: 20, qrbox: 500 }
        );
    }

    html5QrcodeScanner.render(onScanSuccess);
});

function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scan result: ${decodedText}`, decodedResult);

    document.getElementById("result").innerHTML = `
        <p><a href="${decodedText}" target="_blank">Go to Link</a></p>
    `;

    html5QrcodeScanner.clear();
}

