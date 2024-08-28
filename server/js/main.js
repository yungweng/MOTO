checkIFNFCSupported();
function checkIFNFCSupported(){
  if (!("NDEFReader" in window)) {
    alert("NFC is not supported.");
    document.getElementById("NFC-btn").disabled = true;
  }
}
let ndef;
let abortController;
let NFCResults = [];
async function scanNFCTags(){
  if (!ndef) {
    abortController = new AbortController();
    abortController.signal.onabort = event => {
      // All NFC operations have been aborted.
      console.log(event);
    };
    ndef = new NDEFReader();
    ndef.onreadingerror = () => {
      console.log("Cannot read data from the NFC tag. Try another one?");
    };
    ndef.onreading = event => {
      console.log("NDEF message read.");
      console.log(event);
      NFCResults = [];
      NFCResults = NFCResults.concat(event.message.records);
      displayNFCResults();
    };
  }
  ndef.scan({ signal: abortController.signal }).then(() => {
    console.log("Scan started successfully.");
  }).catch(error => {
    console.log(`Error! Scan failed to start: ${error}.`);
  });
}

function toggleNFCScanning(){
  const btn = document.getElementById("NFC-btn");
  if (btn.innerText === "Scan NFC Tags") {
    btn.innerText = "Stop Scanning NFC Tags";
    scanNFCTags();
  }else{
    btn.innerText = "Scan NFC Tags";
    abortController.abort();
  }
}

function displayNFCResults(){
  const ol = document.getElementById("NFC-results");
  ol.innerHTML = "";
  for (let index = 0; index < NFCResults.length; index++) {
    const record = NFCResults[index];
    const buf = record.data.buffer;
    const str = new TextDecoder().decode(buf);
    console.log(str);
    const li = document.createElement("li");
    li.innerText = str;
    ol.appendChild(li);
  }
}
