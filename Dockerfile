FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["python", "main.py"]