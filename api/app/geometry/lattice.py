from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Node:
    id: int
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Strut:
    start: int  # id of the first node
    end: int  # id of the second node
    diameter: float


@dataclass(frozen=True)
class Lattice:
    nodes: list[Node]
    struts: list[Strut]


def generate_cubic_lattice(
    nx: int, ny: int, nz: int, cell_size: float, strut_diameter: float
) -> Lattice:
    if min(nx, ny, nz) < 1:
        raise ValueError("nx, ny and nz must be at least 1")
    if cell_size <= 0 or strut_diameter <= 0:
        raise ValueError("cell_size and strut_diameter must be positive")

    xs = np.arange(nx + 1) * cell_size
    ys = np.arange(ny + 1) * cell_size
    zs = np.arange(nz + 1) * cell_size
    gx, gy, gz = np.meshgrid(xs, ys, zs, indexing="ij")
    coords = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=1)

    ids = np.arange(len(coords)).reshape(nx + 1, ny + 1, nz + 1)
    starts = np.concatenate(
        [ids[:-1, :, :].ravel(), ids[:, :-1, :].ravel(), ids[:, :, :-1].ravel()]
    )
    ends = np.concatenate(
        [ids[1:, :, :].ravel(), ids[:, 1:, :].ravel(), ids[:, :, 1:].ravel()]
    )

    nodes = [
        Node(i, float(x), float(y), float(z)) for i, (x, y, z) in enumerate(coords)
    ]
    struts = [
        Strut(int(s), int(e), strut_diameter) for s, e in zip(starts, ends)
    ]
    return Lattice(nodes=nodes, struts=struts)


def total_strut_length(lattice: Lattice) -> float:
    coords = np.array([[n.x, n.y, n.z] for n in lattice.nodes])
    starts = np.array([s.start for s in lattice.struts])
    ends = np.array([s.end for s in lattice.struts])
    return float(np.linalg.norm(coords[ends] - coords[starts], axis=1).sum())