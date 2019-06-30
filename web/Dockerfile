FROM python:alpine3.7
#ENV FLASK_ENV development
#ENV FLASK_APP ui 
COPY templates/ /app/templates/
COPY . /app
#RUN chmod -x /app/ui.py
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "/app/ui.py"]
#CMD ["flask", "run", "-h", "0.0.0.0"]
#CMD ["ping", "test-rabbit", "-c", "999999"]
