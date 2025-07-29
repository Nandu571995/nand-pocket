# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose port for Render
ENV PORT=10000
EXPOSE 10000

# Run the bot
CMD ["python", "main.py"]
