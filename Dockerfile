################################################################################
# Base image
################################################################################
FROM registry.cn-hangzhou.aliyuncs.com/lacogito/tarsier-build-base:latest

WORKDIR /home/mirabox

# Copy application code
COPY tarsier tarsier
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip cache purge

# unstructured model cache
ENV UNSTRUCTURED_DEFAULT_MODEL_NAME=yolox

# Expose API port
EXPOSE 8899

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "tarsier:api_server", "--host", "0.0.0.0", "--port", "8899"]
