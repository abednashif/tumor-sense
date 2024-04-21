FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask app code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=tumor-sense

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]