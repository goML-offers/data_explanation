# FROM python:3.11

# WORKDIR /api/
# COPY . .
# COPY requirements.txt .

# RUN pip install --no-cache-dir --upgrade  -r requirements.txt


# RUN pip install uvicorn
# # RUN /api/app.py

# CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000" ]
# Use a Python base image
FROM python:3.11

# Set the working directory
WORKDIR /redshift/
COPY . .
# Copy the requirements file into the container
COPY requirements.txt .
RUN python3 -m pip install beautifulsoup4 --force-reinstall
RUN pip install python-multipart
# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container

# CMD ["python", "app.py"]
# # Command to run your application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]