# Use the latest stable Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY packages.txt .
RUN pip install --no-cache-dir -r packages.txt

# Copy the rest of the bot's source code
COPY . .

# Run the bot
CMD ["python", "main.py"]
