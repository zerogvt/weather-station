# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /weather

# Copy the current directory contents into the container at /app
COPY . /weather

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
#ENV FLASK_APP=app.py

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
