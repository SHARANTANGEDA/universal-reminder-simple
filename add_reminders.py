import os

import requests
from sqlalchemy import create_engine
import json
from flask import Flask, request
import uuid
import time
from datetime import timedelta

app = Flask(__name__)

db_string = os.getenv("POSTGRES_CONNECTION_STRING")
incoming_webhook = os.getenv("SLACK_WEBHOOK_URL")

db = create_engine(db_string)

SLACK_SUCCESS_COLOR = "good"
SLACK_WARNING_COLOR = "warning"
SLACK_ERROR_COLOR = "danger"


def send_success_alert(title, message, web_hook_url):
    request_body = {
        "attachments": [{
            "title": title,
            "color": SLACK_SUCCESS_COLOR,
            "text": message,
            "ts": time.time()
        }
        ]
    }

    return requests.post(url=web_hook_url, json=request_body)


def send_warning_alert(title, message, web_hook_url):
    request_body = {
        "attachments": [{
            "title": title,
            "color": SLACK_WARNING_COLOR,
            "text": message,
            "ts": time.time()
        }
        ]
    }

    return requests.post(url=web_hook_url, json=request_body)

@app.route("/healthcheck")
def ping():
    return "Pong !"


@app.route('/add-reminders', methods=['POST'])
def add_reminders():
    record = request.json

    remind_after_sec = None
    if record["duration"].endswith("h"):
        remind_after_sec = int(timedelta(hours=int(record["duration"][:-1])).total_seconds())
    elif record["duration"].endswith("d"):
        remind_after_sec = int(timedelta(days=int(record["duration"][:-1])).total_seconds())
    elif record["duration"].endswith("s"):
        remind_after_sec = int(record["duration"][:-1])
    else:
        raise Exception("Duration format is incorrect")


    db.execute(
    f"""
        INSERT INTO event_reminders (reminder_id, reminder_name, reminder_type, reminder_message,
        reminder_after_in_seconds) 
        
        VALUES ('{uuid.uuid4()}','{record["title"]}', '{record["reminder_type"]}','{record["reminder_message"]}', 
        {remind_after_sec})
    """)

    send_success_alert(
        "Event Reminder Configured!",
        f"""
        Title: '{record["title"]}'
        Remind After: '{record["duration"]}'
        Type: '{record["reminder_type"]}'
        
        Message: '{record["reminder_message"]}'
        
        """,
        web_hook_url=incoming_webhook

    )

    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
