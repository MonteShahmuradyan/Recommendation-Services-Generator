# My python update
FROM python:3.11

# working directory
WORKDIR /app

# Copy files into the container
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY generator.py .

# Expose the port of Generator
EXPOSE 5001

# Run the application
CMD ["python", "generator.py"]
