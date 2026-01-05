#!/usr/bin/env python3

import os
import re
import requests
from flask import Flask, request, jsonify, stream_with_context, Response
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080

TIKTOK_REGEX = re.compile(
    r'^(https?:\/\/)?(www\.|vm\.|vt\.|m\.)?tiktok\.com\/.+$',
    re.IGNORECASE
)

TIKTOK_API = "https://tikwm.com/api/"

app = Flask(__name__)

def timestamp():
    return datetime.now().timestamp()

def banner():
    print("""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ 
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ 
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
 TikTok Video Fetch API
""")


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "error": "Permission denied",
        "code": 403,
        "timestamp": timestamp()
    }), 403


@app.route("/api/tiktok", methods=["POST"])
def tiktok_api():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Invalid JSON"}), 400

    url = data["url"].strip()

    if not TIKTOK_REGEX.match(url):
        return jsonify({"error": "Invalid TikTok URL"}), 400

    r = requests.post(
        TIKTOK_API,
        data={"url": url},
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.tiktok.com/"
        },
        timeout=15
    )

    v_data = r.json()
    if not v_data.get("data"):
        return jsonify({"error": "Fetch failed"}), 500

    v_data["developer"] = {
        "name": "Mr Shohid",
        "telegram": "https://t.me/darknexus_bd"
    }

    return jsonify(v_data), 200


def run():
    os.system("clear")
    banner()
    app.run(host=HOST, port=PORT)