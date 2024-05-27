FROM alloranetwork/allora-inference-base:v0.0.7

COPY requirements.txt /app/
RUN pip3 install --requirement /app/requirements.txt

# Copy the main python file so it is accessible to the Allora extension.
COPY main.py /app/

