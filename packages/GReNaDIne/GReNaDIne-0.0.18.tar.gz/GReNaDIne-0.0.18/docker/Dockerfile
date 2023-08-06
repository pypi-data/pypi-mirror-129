# Use an official Python runtime as a parent image
FROM ubuntu

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get -qq update && apt-get -qq -y install python3.7 python3-pip build-essential git
RUN pip3 install cython numpy
RUN pip3 install POT
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

RUN pip3 install grenadine

# Run app.py when the container launches
CMD ["python", "test.py"]
