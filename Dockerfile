# ---- Base Image ----
FROM python:3.11-slim

# ---- Working Dir ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy App ----
COPY converter_service.py .

# ---- Expose Port ----
EXPOSE 10000

# ---- Run ----
CMD ["python", "converter_service.py"]
