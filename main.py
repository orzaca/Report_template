from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 Variables de entorno (se configuran en Render)
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

AUTH_URL = "https://visionlatam.securitas.com/rest/v1/auth"
REPORT_URL = "https://visionlatam.securitas.com/rest/v1/report-templates"

def get_token():
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}
    response = requests.post(AUTH_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["auth"]["token"]

def get_all_reports():
    token = get_token()
    all_data = []
    limit = 100
    for offset in range(0, 6100, 100):  # Ajusta según tu necesidad
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        params = {"limit": limit, "offset": offset}
        response = requests.get(REPORT_URL, headers=headers, params=params)
        response.raise_for_status()
        page_data = response.json().get("data", [])
        if not page_data:
            break
        all_data.extend(page_data)
    return all_data

@app.route("/report-templates", methods=["GET"])
def report_templates():
    data = get_all_reports()
    return jsonify(data)

# Render usa Gunicorn, no este bloque:
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
