FROM python:3.9.14

RUN pip3 install sqlalchemy psycopg2-binary requests flask

RUN mkdir -p /scripts

COPY add_reminders.py /scripts
WORKDIR /scripts

LABEL code_lang=python
EXPOSE 8000

CMD ["python", "add_reminders.py" ]
