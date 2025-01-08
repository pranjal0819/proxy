# Final stage for combining the built frontend and backend
FROM python:3.12-alpine

# Set environment variables
ARG USER=app
ENV HOME=/home/$USER PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH=$PATH:/home/$USER/.local/bin

# Create group "app" and user "app"
RUN addgroup -S $USER && adduser -S -G $USER -h $HOME -s /bin/bash $USER

# Set the working directory in the container
WORKDIR $HOME

# Switch to application user
USER $USER

# Copy the dependencies file to the working directory
COPY --chown=$USER:$USER requirements.txt $HOME

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Django application code
COPY --chown=$USER:$USER . $HOME

# Collect Django admin static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Use gunicorn to serve the application
CMD ["gunicorn", "proxy.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]
