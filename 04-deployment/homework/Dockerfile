FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim
# Set the working directory
WORKDIR /app

COPY requirements.txt .
# Copy the scoring script into the container
RUN pip install --no-cache-dir -r requirements.txt



COPY scoring.py .


# Specify the command to run the script with parameters
CMD ["python", "scoring.py", "--year=2023", "--month=5", "--aws=no"]