from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, Query
from unstructured.partition.auto import partition
import tempfile
import os

from .xlog import xlogger

api_server = FastAPI(
    title="Magic Parser API",
    description="PDF parsing API using unstructured library",
    version="0.1.0",
)

# API Routers for different versions
v1_router = APIRouter(prefix="/api/v1")


@api_server.get("/ping")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "PDF Parser API is running"}


@v1_router.post("/general")
async def parse_file(
    file: UploadFile = File(...),
    with_metadata: bool = Query(
        False, description="Whether to include metadata in the response"
    ),
):

    xlogger.info(f"Received file: {file.filename}")

    # Create a temporary file with appropriate suffix
    file_ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()
        try:
            elements = partition(
                temp_file.name,
                strategy="hi_res",
                skip_infer_table_types=list(),
                hi_res_model_name="yolox",
            )
            result = []
            for element in elements:
                ele_details = dict()
                category = element.category
                ele_details["text"] = element.text
                ele_details["text_as_html"] = element.metadata.text_as_html
                ele_details["category"] = category
                if with_metadata:
                    ele_details["_metadata"] = element.metadata
                result.append(ele_details)

            return {"status": "success", "content": result}
        except Exception as e:
            xlogger.error(f"failed to partition file {file.filename}, error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)


# Include routers
api_server.include_router(v1_router)
