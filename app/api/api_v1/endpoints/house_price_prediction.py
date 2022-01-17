from fastapi import APIRouter, Depends, HTTPException
import logging

from api.api_v1.util.auth_logic import Auth
from api.api_v1.schemas.api_schemas import PredictorVariables, HousePrice
from connections.s3_client import S3Client

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/house_price_prediction', response_model=HousePrice, status_code=200)
async def get_house_price_prediction(predictor_variables: PredictorVariables = Depends(),
                                     auth=Depends(Auth().auth_wrapper)) -> HousePrice:
    """Get housing price prediction based on linear regression model stored in S3. Requires a header with user JWT
    bearer token. Return code 500 on unexpected exception and 200 on success.

    Arguments (PredictorVariables):
        - house_surface
        - garden_surface
        - rooms
    """
    try:
        # Get the most recent model from s3
        model = S3Client().read_most_recent_model()

        # Make a single prediction for the given parameters
        prediction = model.predict([[predictor_variables.house_surface, predictor_variables.garden_surface,
                                     predictor_variables.rooms]])[0]
        return HousePrice(price_in_euros=prediction)

    except Exception as e:
        logger.exception(f'Something went wrong getting the model, traceback: {e}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred in the application backend')
