# Use the official Python 3.9.1 image as a base image
FROM python:3.9.1

# Set the working directory in the container to /app
WORKDIR /app

# Install wget using apt-get
# The -y option for apt-get install assumes 'yes' to all prompts
# Update the package index before installing to get the latest version
RUN apt-get update && apt-get install -y wget

# Install the required Python libraries
# It is a good practice to use `--no-cache-dir` flag with pip install to keep the Docker image size down
RUN pip install --no-cache-dir pandas sqlalchemy pyarrow psycopg2-binary tqdm

# Copy the ingest_data.py script from the current directory to /app in the container
COPY ingest_data.py .

# When the container starts, run the ingest_data.py script
ENTRYPOINT ["python", "ingest_data.py"]