import os
import time
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder=".")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
CONTACT_USER_ID = "1559815109071732808"
DISCORD_API = "https://discord.com/api/v10"
last_submission = {}

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.post("/api/apply")
def apply():
    # Basic per-IP cooldown to reduce spam; no application data is stored.
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    now = time.time()
    if now - last_submission.get(ip, 0) < 20:
        return jsonify(error="너무 빠른 연속 제출입니다. 20초 뒤 다시 시도해 주세요."), 429

    if not BOT_TOKEN:
        return jsonify(error="서버에 DISCORD_BOT_TOKEN 설정이 없습니다."), 503

    data = request.get_json(silent=True) or {}
    discord_name = str(data.get("discord", "")).strip()[:80]
    age = str(data.get("age", "")).strip()[:30] or "미기재"
    department = str(data.get("department", "")).strip()[:100]
    position = str(data.get("position", "")).strip()[:100]
    experience = str(data.get("experience", "")).strip()[:1000] or "미기재"
    motivation = str(data.get("motivation", "")).strip()[:1200]

    if not discord_name or not department or not position or not motivation:
        return jsonify(error="필수 입력란을 모두 작성해 주세요."), 400

    content = (
        "📨 **영원 ETERNITY 관리진 지원서**\n"
        f"**디스코드 사용자명:** {discord_name}\n"
        f"**나이:** {age}\n"
        f"**지원 부서:** {department}\n"
        f"**희망 직책:** {position}\n"
        f"**관련 경험:** {experience}\n\n"
        f"**지원 동기:**\n{motivation}"
    )
    if len(content) > 1950:
        content = content[:1940] + "\n…(내용이 길어 일부 생략됨)"

    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    try:
        dm_response = requests.post(
            f"{DISCORD_API}/users/@me/channels",
            headers=headers,
            json={"recipient_id": CONTACT_USER_ID},
            timeout=12,
        )
        if dm_response.status_code not in (200, 201):
            app.logger.error("Discord create-DM failed: %s %s", dm_response.status_code, dm_response.text[:300])
            return jsonify(error="디스코드 DM 채널을 열 수 없습니다. 봇 토큰 및 담당자의 DM 설정을 확인해 주세요."), 502

        channel_id = dm_response.json().get("id")
        send_response = requests.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=headers,
            json={"content": content, "allowed_mentions": {"parse": []}},
            timeout=12,
        )
        if send_response.status_code not in (200, 201):
            app.logger.error("Discord send-message failed: %s %s", send_response.status_code, send_response.text[:300])
            return jsonify(error="DM 전송이 거절되었습니다. 봇이 담당자에게 DM을 보낼 수 있는지 확인해 주세요."), 502

        last_submission[ip] = now
        return jsonify(ok=True)
    except requests.RequestException:
        app.logger.exception("Discord API request failed")
        return jsonify(error="디스코드 연결에 실패했습니다. 잠시 후 다시 시도해 주세요."), 502

if __name__ == "__main__":
    # Use a production WSGI server and HTTPS when publishing publicly.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
