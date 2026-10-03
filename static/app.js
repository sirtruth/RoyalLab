async function updateStatus() {
    const response = await fetch("/api/status");
    const data = await response.json();

    const cpu = document.getElementById("cpu-value");
    cpu.textContent = data.cpu;

    const memory = document.getElementById("memory-value");
    memory.textContent = data.memory_used;

    const disk = document.getElementById("disk-value");
    disk.textContent = data.disk_used;

    const memoryMeter = document.getElementById("memory-meter");
    memoryMeter.style.width =
        (data.memory_used / data.memory_total) * 100 + "%";

    const diskMeter = document.getElementById("disk-meter");
    diskMeter.style.width =
        (data.disk_used / data.disk_total) * 100 + "%";
}

async function updateLogs() {
    const response = await fetch("/api/logs");
    const data = await response.json();

    const log = document.querySelector(".system-log");

    log.innerHTML = "";

    data.logs.forEach(function(message) {
        const entry = document.createElement("div");
        entry.className = "log-entry";

        const time = document.createElement("span");
        time.className = "log-time";
        time.textContent = "SSH";

        const msg = document.createElement("span");
        msg.className = "log-message";
        msg.textContent = message;

        entry.appendChild(time);
        entry.appendChild(msg);
        log.appendChild(entry);
    });
}

window.addEventListener("load", function() {
    updateStatus();
    updateLogs();

    setInterval(updateStatus, 5000);
    setInterval(updateLogs, 5000);
});
