# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install any dependencies required for the app
# (Make sure requirements.txt contains all your dependencies)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

# Step 6: Define the command to run your app (Streamlit app)
CMD ["streamlit", "run", "app.py"]