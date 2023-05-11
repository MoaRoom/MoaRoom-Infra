from typing import Optional, List
from pydantic import BaseModel


class PortModel(BaseModel):
    name: str
    containerPort: int
    protocol: str


class ContainerModel(BaseModel):
    name: str
    image: str
    ports: List[PortModel]  # [{ containerPort: 80, protocol: TCP }]


class PodModel(BaseModel):
    name: str
    namespace: str
    containers: List[ContainerModel]
    status_phase: str  # Running
    hostIP: str
    podIP: str
