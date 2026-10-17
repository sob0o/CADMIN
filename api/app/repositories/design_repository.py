from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.geometry.lattice import Lattice
from app.models import Design, Node, Strut
from app.schemas import DesignCreate


def create(db: Session, data: DesignCreate, lattice: Lattice) -> Design:
    design = Design(**data.model_dump())
    db.add(design)
    db.flush()

    node_rows = [
        Node(design_id=design.id, number=n.id, x=n.x, y=n.y, z=n.z)
        for n in lattice.nodes
    ]
    db.add_all(node_rows)
    db.flush()

    id_by_number = {row.number: row.id for row in node_rows}
    db.add_all(
        Strut(
            design_id=design.id,
            start_node_id=id_by_number[s.start],
            end_node_id=id_by_number[s.end],
            diameter=s.diameter,
        )
        for s in lattice.struts
    )
    db.commit()
    return get(db, design.id)


def get(db: Session, design_id: int) -> Design | None:
    query = (
        select(Design)
        .where(Design.id == design_id)
        .options(selectinload(Design.nodes), selectinload(Design.struts))
    )
    return db.execute(query).scalar_one_or_none()


def list_all(db: Session) -> list[Design]:
    return list(db.execute(select(Design).order_by(Design.id)).scalars())