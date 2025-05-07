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
ENV HF_HUB_CACHE=/home/mirabox/model_cache
ENV UNSTRUCTURED_DEFAULT_MODEL_NAME=yolox_quantized

# Preload dependent models
COPY preload_model.py .
COPY testdata/embedded-images.pdf testdata/embedded-images.pdf

RUN python preload_model.py || exit 1

# Expose API port
EXPOSE 8899

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "tarsier:api_server", "--host", "0.0.0.0", "--port", "8899"]
