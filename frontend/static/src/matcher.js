// using someone else's library
let qrCodeReader = null;

let milkID = "";
let patientID = "";

function showQrScannerModal(onSuccessCallback) {

  const modalOverlay = document.createElement("div");
  modalOverlay.id = "qr-scanner-modal-overlay";
  modalOverlay.style.position = "fixed";
  modalOverlay.style.top = "0";
  modalOverlay.style.left = "0";
  modalOverlay.style.width = "100%";
  modalOverlay.style.height = "100%";
  modalOverlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
  modalOverlay.style.display = "flex";
  modalOverlay.style.justifyContent = "center";
  modalOverlay.style.alignItems = "center";
  modalOverlay.style.zIndex = "1000";

  const modalContent = document.createElement("div");
  modalContent.id = "qr-scanner-modal-content";
  modalContent.style.position = "relative";
  modalContent.style.width = "600px";
  modalContent.style.height = "497px";
  modalContent.style.backgroundColor = "#ffffff";
  modalContent.style.padding = "20px";
  modalContent.style.borderRadius = "8px";
  modalContent.style.display = "flex";
  modalContent.style.flexDirection = "column";
  modalContent.style.justifyContent = "center";
  modalContent.style.alignItems = "center";

  const qrReaderDiv = document.createElement("div");
  qrReaderDiv.id = "qr-reader";
  qrReaderDiv.style.width = "100%";
  qrReaderDiv.style.height = "100%";
  modalContent.appendChild(qrReaderDiv);

  const cancelButton = document.createElement("button");
  cancelButton.textContent = "Cancel";
  cancelButton.style.marginTop = "10px";
  cancelButton.addEventListener("click", cancelReader);
  
  function cancelReader() {
    if (qrCodeReader) {
      qrCodeReader.stop().then(() => {
        qrCodeReader.clear();
        modalOverlay.remove();
        qrCodeReader = null;
      }).catch(err => {
        console.error("Error stopping the scanner:", err);
      });
    }
  };

  modalContent.appendChild(cancelButton);
  modalOverlay.appendChild(modalContent);
  document.body.appendChild(modalOverlay);

  setTimeout(() => {
    qrCodeReader = new Html5Qrcode("qr-reader");

    const config = {
      fps: 10,
      qrbox: { width: 500, height: 500 }
    };

    qrCodeReader.start(
        { facingMode: "environment" },
        config,
        (decodedText) => {
          onSuccessCallback(decodedText);
          cancelReader();
        }
    ).catch((err) => {
        console.error("Unable to start QR scanner:", err);
        modalOverlay.remove();
    });
  }, 500);
}

function scanMilkQRCode() {
  showQrScannerModal((decodedText) => {
    milkQrCodeData = decodedText;
    milkID = decodedText.substr(decodedText.length - 36);
    const scanMilkButton = document.querySelector("button:nth-child(1)");
    scanMilkButton.classList.add("scan-success");
  });
}

function scanPatientQRCode() {
  showQrScannerModal((decodedText) => {
      patientQrCodeData = decodedText;
      patientID = decodedText.substr(decodedText.legnth - 10);
      const scanMilkButton = document.querySelector("button:nth-child(2)");
    scanMilkButton.classList.add("scan-success");
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  const scanMilkButton = document.querySelector("button:nth-child(1)");
  const scanPatientButton = document.querySelector("button:nth-child(2)");
  const checkButton = document.querySelector("button:nth-child(3)");

  scanMilkButton.addEventListener("click", scanMilkQRCode);
  scanPatientButton.addEventListener("click", scanPatientQRCode);

  checkButton.addEventListener("click", async () => {
      if (milkQrCodeData && patientQrCodeData) {
        const url = `http://localhost:5500/validate?milk_id=${milkID}&baby_id=${patientID}`;
        const valid = await get(url);
        if (valid) {
          window.location.href = "http://localhost:5500/match";
        } else {
          window.location.href = "http://localhost:5500/notmatch";
        }
      } else {
        alert("Please scan both QR codes first.");
      }
  });
});

async function get(url) {
  try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Error: ${response.statusText}`);
      const result = await response.json();
      return result.status === "Milk is safe for baby";
  } catch (error) {
      console.error("Error fetching data:", error);
      return false;
  }
}