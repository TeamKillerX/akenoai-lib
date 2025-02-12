import logging
import os

import uvicorn
from fastapi import Depends, HTTPException
from akenoai import AkenoXToJs as _ran_dev

app = _ran_dev.get_app()

logger = logging.getLogger(__name__)
LOGS = logging.getLogger("[akenox]")
logger.setLevel(logging.DEBUG)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/test")
async def example_json():
    response = _ran_dev.fasthttp.get("https://jsonplaceholder.typicode.com/todos/1").json()
    title = _ran_dev.dict_to_obj(response).title
    return {"message": title}

@app.get("/api/openai/gpt-old")
async def get_openai(query: str):
    return await _ran_dev.randydev(
        "ai/openai/gpt-old",
        custom_dev_fast=True,
        query=query
    )

@app.post("/item/users")
async def add_item(add: str, number: int):
    return {"message": f"{add} & {number}"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = _ran_dev.get_custom_openai(
        title="AkenoX AI API",
        version="1.0.0",
        summary="Use It Only For Personal Project",
        description="Free API By akenoai-lib",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://github-production-user-asset-6210df.s3.amazonaws.com/90479255/289277800-f26513f7-cdf4-44ee-9a08-f6b27e6b99f7.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

def run_fast(build=app, host: str = '0.0.0.0', port: int = 8000) -> None:
    LOGS.info(f"Running on port {port}")
    uvicorn.run(build, host=host, port=port)
    LOGS.info(f"Closing port {port}")
