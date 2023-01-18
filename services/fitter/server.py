import uvicorn
import matplotlib

from pydantic import Json
from pandas import read_csv
from decouple import config, Csv
from fastapi import FastAPI, APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import Response

from .._models.options import Options
from .._utils.exceptions import InvalidRequestError

from .service import service


def fitter_router() -> APIRouter:
    fitter_router = APIRouter(prefix="/fitter")

    @fitter_router.post(
        "/",
        responses={200: {"content": {"image/png": {}}}},
        # Prevent FastAPI from adding "application/json" as an additional
        # response media type in the autogenerated OpenAPI specification.
        # https://github.com/tiangolo/fastapi/issues/3258
        response_class=Response,
    )
    def fit_request(
        rawData: UploadFile = File(...),
        rawOptions: Json[Options] = Form(...),
        rawFunc: str = Form(),
    ):
        try:
            data = read_csv(rawData.file, sep=",", index_col=0)
            plot_img = service(data, rawOptions, rawFunc)
        except (InvalidRequestError, ValueError) as e:
            raise HTTPException(status_code=400, detail="Bad request: " + str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Oops my bad: " + str(e))
        return Response(plot_img, media_type="image/png")

    return fitter_router


def app():
    app = FastAPI()

    origins = [
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    host, port, log_level = config("FITTER_SERVER", cast=Csv())
    uvicorn.run(
        "server:app", host=host, port=int(port), log_level=log_level, reload=True
    )
