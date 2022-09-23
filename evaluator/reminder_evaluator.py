import requests
import os
from sqlalchemy import create_engine, Boolean, Column, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask
import time
from datetime import datetime, timedelta

app = Flask(__name__)

db_string = os.getenv("POSTGRES_CONNECTION_STRING")
incoming_webhook = os.getenv("SLACK_WEBHOOK_URL")


db = create_engine(db_string)
Base = declarative_base()

SLACK_SUCCESS_COLOR = "good"
SLACK_WARNING_COLOR = "warning"
SLACK_ERROR_COLOR = "danger"


class EventReminder(Base):
    __tablename__ = 'event_reminders'

    reminder_id = Column(String, primary_key=True)
    reminder_name = Column(String, nullable=False)
    reminder_type = Column(String, nullable=False)
    reminder_created_at = Column(DateTime, default=str(datetime.now()))
    reminder_active = Column(Boolean, default=True)
    reminder_done = Column(Boolean, default=True)
    reminder_last_n_days = Column(BigInteger, default=5)
    reminder_after_in_seconds = Column(BigInteger, nullable=False)
    reminder_message = Column(String, nullable=False)


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


def send_error_alert(title, message, web_hook_url):
    request_body = {
        "attachments": [{
            "title": title,
            "color": SLACK_ERROR_COLOR,
            "text": message,
            "ts": time.time()
        }
        ]
    }

    return requests.post(url=web_hook_url, json=request_body)


def check_and_raise_alert(record):
    current_time = datetime.now()
    days_remaining = (record.reminder_created_at - current_time +
                      timedelta(seconds=record.reminder_after_in_seconds)).days

    if record.reminder_last_n_days >= days_remaining > 0:
        print(f"Raise Expiry Warning Alert, {record.reminder_message}")
        send_warning_alert(
            title=f"{record.reminder_name}: Expires in {days_remaining} days",
            message=record.reminder_message,
            web_hook_url=incoming_webhook
        )
    elif days_remaining <= 0:
        print(f"Raise Expired Alert, {record.reminder_message}")

        send_error_alert(
            title=f"[EXPIRY_ALERT] {record.reminder_name} expired!!",
            message=record.reminder_message,
            web_hook_url=incoming_webhook
        )


session = sessionmaker(bind=db)()
records = session.query(EventReminder).filter_by(reminder_done=False, reminder_active=True).all()

for record in records:
    check_and_raise_alert(record)
