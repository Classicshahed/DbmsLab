import os
import sys
import time
import subprocess
import threading
from werkzeug.serving import make_server

BASE_DIR = r"C:\Users\USER\.gemini\antigravity\scratch\dbms_Lab_project"
sys.path.insert(0, BASE_DIR)

import app as app_module
from app import app
from flask import request, session

@app.route("/screenshot/admin")
def screenshot_admin():
    session[app_module.ADMIN_SESSION_FLAG] = True
    return app_module.admin_pending()

@app.route("/screenshot/profile")
def screenshot_profile():
    session[app_module.ADMIN_SESSION_FLAG] = True
    return app_module.profile()

class ServerThread(threading.Thread):
    def __init__(self, app, host='127.0.0.1', port=5000):
        super().__init__()
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def capture_screenshots():
    server = ServerThread(app, '127.0.0.1', 5000)
    server.start()
    time.sleep(1.5)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    out_dir = os.path.join(BASE_DIR, "Project_Report", "Project_Screenshots")
    os.makedirs(out_dir, exist_ok=True)

    targets = [
        ("01_dashboard.png", "http://127.0.0.1:5000/"),
        ("02_donors_list.png", "http://127.0.0.1:5000/donors"),
        ("03_donor_form.png", "http://127.0.0.1:5000/donors/new"),
        ("04_donor_history.png", "http://127.0.0.1:5000/donors/1/donations"),
        ("05_donations_list.png", "http://127.0.0.1:5000/donations"),
        ("06_stock_inventory.png", "http://127.0.0.1:5000/stock"),
        ("07_hospitals_list.png", "http://127.0.0.1:5000/hospitals"),
        ("08_hospital_form.png", "http://127.0.0.1:5000/hospitals/new"),
        ("09_requests_management.png", "http://127.0.0.1:5000/requests"),
        ("10_sql_reports.png", "http://127.0.0.1:5000/reports"),
        ("11_admin_login.png", "http://127.0.0.1:5000/admin/login"),
        ("12_admin_pending.png", "http://127.0.0.1:5000/screenshot/admin"),
        ("13_admin_profile.png", "http://127.0.0.1:5000/screenshot/profile"),
    ]

    for fname, url in targets:
        out_path = os.path.join(out_dir, fname)
        cmd = [
            edge_path,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1280,960",
            f"--screenshot={out_path}",
            url
        ]
        print(f"Capturing {fname} from {url}...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)

    server.shutdown()
    print("All screenshots captured successfully.")

if __name__ == "__main__":
    capture_screenshots()
