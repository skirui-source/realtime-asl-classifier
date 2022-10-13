# Step: Install official Python base image
FROM python:3.8

# Step: Set working directory inside the container
WORKDIR /myapp

# Step: Install appropriate dependencies
RUN apt-get -y update  && apt-get install -y \
    python3-dev \
    apt-utils \
    python-dev \
    build-essential \   
&& rm -rf /var/lib/apt/lists/* 

# Step: Copy everything to workdir inside container
COPY . /myapp

# Step: Install required python dependencies from requirements file
RUN pip install --no-cache-dir -U -r  /myapp/requirements.txt

# Step: Expose the port Flask is running on
EXPOSE 5000

# Step: Run Flask
CMD python3 app.py