from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DesignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    nx: int = Field(ge=1, le=20)
    ny: int = Field(ge=1, le=20)
    nz: int = Field(ge=1, le=20)
    cell_size: float = Field(gt=0)
    strut_diameter: float = Field(gt=0)


class NodeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    x: float
    y: float
    z: float


class StrutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    start_node_id: int
    end_node_id: int
    diameter: float


class DesignSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    nx: int
    ny: int
    nz: int
    cell_size: float
    strut_diameter: float
    created_at: datetime


class DesignDetail(DesignSummary):
    nodes: list[NodeOut]
    struts: list[StrutOut]