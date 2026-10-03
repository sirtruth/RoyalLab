from flask import Flask, render_template
import socket
import subprocess
import os
import shutil

app = Flask(__name__)


server_name = socket.gethostname()

def get_status():
    return "ONLINE"

def get_uptime():
    result = subprocess.run(
        ["uptime", "-p"],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def get_cpu():
    with open("/proc/stat") as file:

        line = file.readline()

    values = line.split()[1:]

    total = sum(map(int, values))

    idle = int(values[3])

    return round((1 - idle / total) * 100, 1)

def get_memory():
    with open("/proc/meminfo") as file:
        data = file.readlines()

    memory = {}

    for line in data:
        key, value = line.split(":")
        memory[key] = int(value.strip().split()[0])

    total = memory["MemTotal"]
    available = memory["MemAvailable"]

    used = total - available

    return round(used / 1024 / 1024, 2), round(total / 1024 / 1024, 2)

def get_disk():
    disk = shutil.disk_usage("/")
    
    used = disk.used / 1024 / 1024 / 1024
    total = disk.total / 1024 / 1024 / 1024

    return round(used, 2), round(total, 2)

@app.route("/")
def home():
    memory_used, memory_total = get_memory()
    memory_percent = round((memory_used / memory_total) * 100, 1)
    
    disk_used, disk_total = get_disk()
    disk_percent = round((disk_used / disk_total) * 100, 1)
    
    return render_template(
        "index.html",
        server_name=server_name,
        status=get_status(),
        uptime=get_uptime(),
        cpu=get_cpu(),
        memory_used=memory_used,
        memory_total=memory_total,
        memory_percent=memory_percent,
        disk_used=disk_used,
        disk_total=disk_total,
        disk_percent=disk_percent
    )

@app.route("/api/status")
def api_status():
    memory_used, memory_total = get_memory()
    disk_used, disk_total = get_disk()

    return {
        "server": server_name,
        "status": get_status(),
        "uptime": get_uptime(),
        "cpu": get_cpu(),
        "memory_used": memory_used,
        "memory_total": memory_total,
        "disk_used": disk_used,
        "disk_total": disk_total
    }
@app.route("/api/logs")
def api_logs():
    result = subprocess.run(
        ["journalctl", "-u", "ssh", "--since", "10 minutes ago", "--no-pager", "-o", "short-iso"],
        capture_output=True,
        text=True,
        timeout=3,
        check=False
    )

    logs = result.stdout.strip().splitlines()

    return {"logs": logs[-25:]}
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/api/security")
def api_security():
    import subprocess

    try:
        result = subprocess.run(
            ["journalctl", "-u", "ssh", "--since", "today", "--no-pager"],
            capture_output=True,
            text=True,
            timeout=5
        )

        lines = result.stdout.splitlines()

        failed = [
            line for line in lines
            if "Failed password" in line or "authentication failure" in line
        ]

        return {
            "ssh_failed_attempts": len(failed),
            "recent_attempts": failed[-10:]
        }

    except Exception as e:
        return {
            "error": str(e)
        }