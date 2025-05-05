# Magic Parser API

A FastAPI-based HTTP API server for parsing PDF files using the unstructured library.

## Setup

### Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn tarsier:api_server --port 8899 --reload
   ```

## API Endpoints

### Base Endpoints
- `GET /ping`: Health check endpoint

### V1 Endpoints
- `POST /api/v1/general`: Universal parser for various file types (PDF, images, etc.)

## Example Usage

### Parse Any File (PDF/Image)

```bash
curl -X POST "http://localhost:8899/api/v1/general" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

Response data:

```json
{
  "status": "success",
  "content": [
    {
      "type": "<element_type>",
      "text": "<extracted_text>",
      "metadata": {}
    }
  ],
  "metadata": {
    "file_type": "<mime_type>",
    "chunking_strategy": "<strategy>",
    "content_type_hint": "<content_type>",
    "encoding": "<encoding>"
  }
}
```
