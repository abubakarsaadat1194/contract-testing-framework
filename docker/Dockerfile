FROM python:3.11

WORKDIR /app

COPY ../provider /app/provider

RUN pip install flask

EXPOSE 5000

CMD ["python", "provider/user_service.py"]