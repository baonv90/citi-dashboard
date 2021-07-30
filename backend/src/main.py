import logging
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends

from .model import Device, generate_device
from .paginator import Page, Paginate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = FastAPI(title="Quizz backend", version="1.0", debug=True)

# For React front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/device/{vid}", name="get_device", response_model=Device)
async def get_device(request: Request, vid: int):
    return generate_device(request=request, vid=vid)


@app.get("/devices", response_model=Paginate(Device))
async def devices(request: Request, page: Page = Depends()):
    total_devices = 1000
    bottom: int = page.offset
    top: int = min(page.offset + page.limit, total_devices)
    devices_list: List[Device] = [
        generate_device(request, i) for i in range(bottom, top)
    ]

    return page.build(results=devices_list, total_results=total_devices)
