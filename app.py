from flask import Flask, render_template, request, redirect, url_for, session
import socket
import subprocess
import os
import shutil
from werkzeug.security import check_password_hash
from auth_config import USERNAME, PASSWORD_HASH, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@app.before_request
def require_login():
    if request.endpoint in ("login", "static"):
        return

    if not session.get("logged_in"):
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session.clear()
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))




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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
