import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Fetch container name from environment variable (injected by K8s)
CONTAINER_NAME = os.getenv("CONTAINER_NAME", "Unknown-Container")

def get_tel_aviv_temp():
    try:
        # Using open-meteo free API for Tel Aviv coordinates
        url = "https://api.open-meteo.com/v1/forecast?latitude=32.0853&longitude=34.7818&current_weather=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data["current_weather"]["temperature"]
        return f"{temp}°C"
    except Exception:
        return "Unavailable"

@app.route('/')
def home():
    # Capture the real client IP if behind a proxy/ingress
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # If multiple IPs are in the header, take the first one
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
        
    temperature = get_tel_aviv_temp()
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Silverfort Challenge</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f6f9; color: #333; }
            .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
            h1 { color: #0052cc; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Silverfort Technical Challenge</h1>
            <p>Hello <strong>{{ client_ip }}</strong> and welcome to Silverfort's <strong>{{ container_name }}</strong>,</p>
            <p>Current Temperature in Tel-Aviv is <strong>{{ temperature }}</strong></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, client_ip=client_ip, container_name=CONTAINER_NAME, temperature=temperature)

if __name__ == '__main__':
    # Running on port 5000 internally
    app.run(host='0.0.0.0', port=5000)