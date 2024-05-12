FROM python:3.11

RUN python3 -m pip install flask

RUN mkdir /app

# Set the working directory in the container
WORKDIR /app

#RUN apt-get update
#RUN apt-get install sudo -y
#RUN sudo apt-get update -y
#RUN sudo apt-get install -y unixodbc-dev

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the entire Flask app code into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 8001

# Set the environment variable for Flask
ENV FLASK_APP=TumorSense

# Run the Flask app when the container starts
#CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python", "app.py", "--host=0.0.0.0", "--port", "8001"]