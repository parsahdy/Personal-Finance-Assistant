FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "Finance_project.wsgi:application", "--bind", "0.0.0.0:8000"]