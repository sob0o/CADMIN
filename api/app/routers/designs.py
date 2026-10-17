from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import DesignCreate, DesignDetail, DesignSummary
from app.services import design_service

router = APIRouter(prefix="/designs", tags=["designs"])


@router.post("", response_model=DesignDetail, status_code=201)
def create_design(data: DesignCreate, db: Session = Depends(get_db)):
    return design_service.create_design(db, data)


@router.get("", response_model=list[DesignSummary])
def list_designs(db: Session = Depends(get_db)):
    return design_service.list_designs(db)


@router.get("/{design_id}", response_model=DesignDetail)
def get_design(design_id: int, db: Session = Depends(get_db)):
    design = design_service.get_design(db, design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    return design