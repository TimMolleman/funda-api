from fastapi import FastAPI
from mangum import Mangum
import uvicorn

from api.api_v1.api import router as api_router

# Init app
app = FastAPI(openapi_prefix='/prod')


# Root route
@app.get('/')
async def root():
    return {'message': 'This is the root page for the API for requesting Funda housing data'}


# Include routers and create mangum handler
app.include_router(api_router, prefix='/api/v1')
handler = Mangum(app)

if __name__ == '__main__':
    # Local run setup for the FastAPI application
    uvicorn.run(app='api_handler:app', port=8000, reload=True)
