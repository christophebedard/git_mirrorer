FROM python:3-slim

# Install git (not included in -slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
        git

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define these environment variables with -e
#ENV ORIGIN_URL
#ENV DESTINATION_URL
#ENV BRANCHES_LIST
#ENV UPDATE_PERIOD

# Run when the container launches
CMD ["python", "git_mirrorer.py"]