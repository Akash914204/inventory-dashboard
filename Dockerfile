# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
