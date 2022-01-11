from fastapi import APIRouter

from .endpoints import auth
from .endpoints import house_price_prediction
from .endpoints import house_to_database
from .endpoints import get_house_data

# Create router and include the endpoints
router = APIRouter()
router.include_router(auth.router, tags=['Auth Endpoints'])
router.include_router(house_price_prediction.router, tags=['House Price Prediction'])
router.include_router(house_to_database.router, tags=['House To Database'])
router.include_router(get_house_data.router, tags=['Get House Data'])
