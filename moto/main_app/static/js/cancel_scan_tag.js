checkIFNFCSupported();
function checkIFNFCSupported(){
    if (!("NDEFReader" in window)) {
        //alert("NFC is not supported.");
        //document.getElementById("NFC-btn").disabled = true;
    }else{
        //alert("NFC is supported.");
        //document.getElementById("NFC-btn").disabled = false;
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
        };
    }
    ndef.addEventListener("reading", ({ message, serialNumber }) => {
        //const textDecoder = new TextDecoder();
        //document.getElementById('tag_id').value = textDecoder.decode(message.records[0].data);
        //document.getElementById('form').submit();
        console.log(message.records);
    });
    ndef.scan({ signal: abortController.signal }).then(() => {
        console.log("Scan started successfully.");
    }).catch(error => {
        console.log(`Error! Scan failed to start: ${error}.`);
    });
}

function toggleNFCScanning(){
    const btn = document.getElementById("HeadingPNG");
        scanNFCTags();
}

document.addEventListener('DOMContentLoaded', (event) => {
    navigator.permissions.query({ name: "nfc" }).then(permissionStatus => {
        console.log(`NFC user permission: ${permissionStatus.state}`);
        if (permissionStatus.state === 'prompt') {
            
        } else if (permissionStatus.state === 'granted') {
            toggleNFCScanning();
        }
    });    
});