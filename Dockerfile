FROM ubuntu:latest

# Install Cron, update system
RUN apt-get update && apt-get -y install python3 python3-pip 

# Copy over project directory
ADD ./ /remodel

# Install package dependencies
RUN pip install --no-cache-dir -r /remodel/requirements.txt

WORKDIR /remodel

# Give permission to run scripts
RUN chmod +x /remodel/api.py /remodel/wsgi.py /remodel/app.py

# Run the command on container startup
CMD /remodel/wsgi.py