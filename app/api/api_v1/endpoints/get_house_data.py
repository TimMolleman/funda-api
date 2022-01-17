from fastapi import APIRouter, Depends, HTTPException
import logging

from api.api_v1.util.auth_logic import Auth
from api.api_v1.schemas.api_schemas import PriceRange, HouseDataReturn
from connections.funda_db import FundaDB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/get_house_data', response_model=HouseDataReturn, status_code=200)
async def get_house_data(price_range: PriceRange = Depends(), auth=Depends(Auth().auth_wrapper)) -> HouseDataReturn:
    """Get house data records from the funda database. Requires a header with user JWT bearer token. Return code 500
    on unexpected exception and 200 on success.

    Arguments (PriceRange):
        - lower_price (optional)
        - upper_price (optional)
    """
    try:
        result = FundaDB().get_house_rows(price_range.lower_price, price_range.upper_price)

    except Exception as e:
        logger.exception(f'Something went wrong querying the database, traceback: {e}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred in the application backend')

    result = [dict(row) for row in result if row['city']]
    return HouseDataReturn(data=result)
