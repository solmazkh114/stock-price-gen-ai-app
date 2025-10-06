from loguru import logger
import uvicorn

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)


