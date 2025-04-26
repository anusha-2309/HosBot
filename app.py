from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

SLACK_VERIFICATION_TOKEN = "your-slack-verification-token"

@app.route("/slack/command", methods=["POST"])
def slack_command():
    token = request.form.get('token')
    if token != SLACK_VERIFICATION_TOKEN:
        return "Invalid Slack verification token", 403

    command = request.form.get('command')

    if command == "/status":
        output = subprocess.check_output(["bash", "server_scripts/check_status.sh"]).decode('utf-8')
    elif command == "/restart":
        output = subprocess.check_output(["bash", "server_scripts/restart_service.sh"]).decode('utf-8')
    elif command == "/update":
        output = subprocess.check_output(["bash", "server_scripts/update_system.sh"]).decode('utf-8')
    else:
        output = "Unknown command."

    return jsonify({
        "response_type": "in_channel",
        "text": output
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)