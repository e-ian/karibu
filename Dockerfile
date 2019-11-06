FROM python:3.6
WORKDIR /app
COPY requirements.txt /app
COPY . /app
RUN pwd
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "run.py"]