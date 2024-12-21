FROM python:3.11
WORKDIR /app
COPY . /app
# COPY . /app
# COPY ../requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ../requirements.txt .
CMD ["python", "main.py"]