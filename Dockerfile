FROM python:3.9.2-alpine3.13

# Create and set working directory
WORKDIR /home/app/src

# Copy requirements file
COPY ./requirements.txt /home/app/src/requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ./ /home/app/src

# Expose port
EXPOSE 5000

# Set Flask as the entry point
ENTRYPOINT ["flask"]

# Run Flask application
CMD ["run", "--host=0.0.0.0"]
