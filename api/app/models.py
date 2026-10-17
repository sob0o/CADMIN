from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Design(Base):
    __tablename__ = "designs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    nx: Mapped[int] = mapped_column(Integer)
    ny: Mapped[int] = mapped_column(Integer)
    nz: Mapped[int] = mapped_column(Integer)
    cell_size: Mapped[float] = mapped_column(Float)
    strut_diameter: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    nodes: Mapped[list["Node"]] = relationship(
        back_populates="design", cascade="all, delete-orphan"
    )
    struts: Mapped[list["Strut"]] = relationship(
        back_populates="design", cascade="all, delete-orphan"
    )


class Node(Base):
    __tablename__ = "nodes"
    __table_args__ = (UniqueConstraint("design_id", "number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    design_id: Mapped[int] = mapped_column(
        ForeignKey("designs.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)
    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    z: Mapped[float] = mapped_column(Float)

    design: Mapped["Design"] = relationship(back_populates="nodes")


class Strut(Base):
    __tablename__ = "struts"

    id: Mapped[int] = mapped_column(primary_key=True)
    design_id: Mapped[int] = mapped_column(
        ForeignKey("designs.id", ondelete="CASCADE"), index=True
    )
    start_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id", ondelete="CASCADE"))
    end_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id", ondelete="CASCADE"))
    diameter: Mapped[float] = mapped_column(Float)

    design: Mapped["Design"] = relationship(back_populates="struts")