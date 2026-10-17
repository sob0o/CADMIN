from sqlalchemy.orm import Session

from app.geometry.lattice import generate_cubic_lattice
from app.models import Design
from app.repositories import design_repository
from app.schemas import DesignCreate


def create_design(db: Session, data: DesignCreate) -> Design:
    lattice = generate_cubic_lattice(
        data.nx, data.ny, data.nz, data.cell_size, data.strut_diameter
    )
    return design_repository.create(db, data, lattice)


def get_design(db: Session, design_id: int) -> Design | None:
    return design_repository.get(db, design_id)


def list_designs(db: Session) -> list[Design]:
    return design_repository.list_all(db)