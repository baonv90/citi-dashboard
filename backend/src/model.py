import random
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import Request
from pydantic import AnyHttpUrl, BaseModel, Field


class StatusEnum(Enum):
    disconnected = "disconnected"
    connected = "connected"


class ConnectionTypeEnum(Enum):
    cellular = "cellular"
    ethernet = "ethernet"
    wifi = "wifi"


class Device(BaseModel):
    """Full device object"""

    url: Optional[AnyHttpUrl] = Field(
        None, title="Device URL", description="URL for this ressource"
    )

    status: Optional[StatusEnum] = Field(
        None,
        title="Connection status",
        description="Indicates whether the device is reachable via network",
    )

    last_seen_at: datetime = Field(
        ...,
        title="Last seen",
        description="UTC time when the device was last seen online",
    )

    connection_type: Optional[ConnectionTypeEnum] = Field(
        None,
        title="Connection type",
        description="Indicates which network is in use - cellular, ethernet or wifi",
    )

    mac_wifi: Optional[str] = Field(
        None, title="WiFi MAC", description="WiFi adapter's MAC address"
    )

    sim_id: Optional[int] = Field(
        None, title="SIM ID", description="SIM card ID (if present)"
    )

    voltage: Optional[float] = Field(
        None, title="Voltage", description="Battery voltage"
    )

    serial_number: str = Field(
        None, title="Serial number", description="Device serial number"
    )

    class Config:
        schema_extra = {
            "example": {
                "url": "https://fake.url/487",
                "status": "disconnected",
                "last_seen_at": "2020-07-09T07:44:05.627103+00:00",
                "connection_type": "wifi",
                "mac_wifi": "b8:27:eb:6b:0b:2e",
                "sim_id": None,
                "voltage": None,
                "serial_number": None,
            }
        }


def rand_mac(seed: int = None):
    random.seed(seed)
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def generate_device(request: Request, vid: int = 0) -> Device:
    random.seed(vid)
    random_int = random.randint(1, 100)
    status = StatusEnum("connected") if random_int > 50 else StatusEnum("disconnected")
    if random_int < 33:
        connection_type = ConnectionTypeEnum("cellular")
    elif random_int < 66:
        connection_type = ConnectionTypeEnum("ethernet")
    else:
        connection_type = ConnectionTypeEnum("wifi")

    device: Device = Device(
        url=request.url_for("get_device", **{"vid": vid}),
        status=status,
        last_seen_at=datetime.now(),
        connection_type=connection_type,
        mac_wifi=rand_mac(seed=vid),
        sim_id=random.randint(10000000, 99000000),
        voltage=random.uniform(1.0, 12.0),
        serial_number=f"device_{vid}",
    )
    return device
