from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
import logging

from api.api_v1.util.auth_logic import Auth
from api.api_v1.schemas.api_schemas import HouseVariablesAdd
from connections.funda_db import FundaDB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/house_to_database', response_model=HouseVariablesAdd, status_code=201)
async def post_house_to_database(house_variables: HouseVariablesAdd,
                                 auth=Depends(Auth().auth_wrapper)) -> HouseVariablesAdd:
    """Post housing information to the funda database. Requires a header with user JWT.

    Arguments (HouseVariables):
        - link
        - city
        - house_surface
        - garden_surface
        - rooms
        - price
    """
    try:
        # Try to insert data into house database
        FundaDB().insert_house_data(house_variables.link, house_variables.city, house_variables.house_surface,
                                    house_variables.garden_surface, house_variables.rooms, house_variables.price)
        return house_variables
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Funda listing link already in database')
    except Exception as e:
        logger.exception(f'Something went wrong querying the database, traceback: {e}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred in the application backend')
