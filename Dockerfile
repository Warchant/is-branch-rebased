FROM python:3.6

RUN pip3 install flask requests
ENTRYPOINT ["python3", "/app/isbranchrebased-webhook.py"]
