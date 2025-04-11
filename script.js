function submitIPs() {
    let ips = document.getElementById("ip_input").value.trim();
    if (ips === "") {
        alert("Please enter at least one IP address.");
        return;
    }
    eel.set_ips(ips);
}

function startCapture() {
    eel.start_capture();
}

function stopCapture() {
    eel.stop_capture();
}

function updatePacketRate(rate) {
    document.getElementById("rate").innerText = "Packets/sec: " + rate;
}

function notifyThresholdHit() {
    alert("Threshold hit! Packets saved.");
}

function showMessage(msg) {
    document.getElementById("status").innerText = msg;
}

// Expose functions to Eel
eel.expose(updatePacketRate);
eel.expose(notifyThresholdHit);
eel.expose(showMessage);
