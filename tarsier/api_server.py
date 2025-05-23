from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, Query
from unstructured.partition.auto import partition
from .element import Element
import tempfile
import os
import time

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
    model: str = Query("yolox", description="unstructured's object detection model"),
):
    xlogger.info(f"Received file: {file.filename}, model: {model}")
    start_time = time.time()

    # Create a temporary file with appropriate suffix
    parts = os.path.splitext(file.filename)
    if len(parts) < 2:
        raise HTTPException(
            status_code=500, detail=f"no file extention parsed:{file.filename}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=parts[1].lower()) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()
        try:
            result = await partition_unstructured(temp_file.name, model)
            proc_time = time.time() - start_time
            xlogger.info(f"{file.filename} proccessed in {proc_time:.2f} secs")
            return {"status": "success", "content": result}
        except Exception as e:
            xlogger.error(f"failed to partition file {file.filename}, error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)


async def partition_unstructured(file_name, model_name):
    parts = partition(
        file_name,
        strategy="hi_res",
        skip_infer_table_types=list(),
        hi_res_model_name=model_name,
    )
    result = []
    for part in parts:
        ele = Element(category=part.category, text=part.text)
        if part.metadata is not None:
            setattr(ele, "langs", part.metadata.languages)
            setattr(ele, "page_number", part.metadata.page_number)
            if part.metadata.coordinates:
                setattr(ele, "box", part.metadata.coordinates.points)
            if "text_as_html" in dir(part.metadata):
                setattr(ele, "text_html", part.metadata.text_as_html)
        result.append(ele.model_dump())
    return result


# Include routers
api_server.include_router(v1_router)
