FROM --platform=linux/amd64 696230526504.dkr.ecr.us-east-1.amazonaws.com/allora-inference-base:latest

COPY requirements.txt /app/
RUN pip3 install --requirement /app/requirements.txt

# Copy the main python file so it is accessible to the Allora extension.
COPY main.py /app/

