FROM python:3.12-slim

WORKDIR /app

# Copy common module and requirements
COPY ../common /app/common
COPY requirements.txt .
COPY ../common/requirements.txt ./common_requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r common_requirements.txt

# Copy application code
COPY . .

# Run migrations
RUN python -m alembic upgrade head

# Expose port
EXPOSE 8004

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]