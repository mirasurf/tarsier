################################################################################
# Base image
################################################################################
FROM python:3.11-slim

# Configure apt to use mirrors in China
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# Install system dependencies for OCR and file processing
RUN apt-get update && apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-all \
        poppler-utils \
        libmagic1 \
        libgl1-mesa-glx \
        libsm6 \
        libxext6 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /home/mirabox

# Copy application code
COPY tarsier tarsier
COPY requirements.txt .
COPY preload_model.py .
COPY testdata/embedded-images.pdf testdata/embedded-images.pdf

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

# Preload dependent models
RUN python preload_model.py

# Set timezone
ENV TZ="Asia/Shanghai"

# Expose API port
EXPOSE 8899

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "tarsier:api_server", "--host", "0.0.0.0", "--port", "8899"]
