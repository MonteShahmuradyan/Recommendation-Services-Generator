# My python version
FROM python:3.11

# working directory for container
WORKDIR /app

# Copy the current directory
COPY . /app
COPY static /app/static


# Install the packages for requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5002 usable for outside of the container
EXPOSE 5002

# Run app.py when the container launches
CMD ["python", "invoker.py"]
