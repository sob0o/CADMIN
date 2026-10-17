import pytest

from app.geometry.lattice import generate_cubic_lattice, total_strut_length


def test_single_cell_has_8_nodes_and_12_struts():
    lattice = generate_cubic_lattice(1, 1, 1, 10.0, 2.0)
    assert len(lattice.nodes) == 8
    assert len(lattice.struts) == 12


def test_counts_for_a_larger_grid():
    nx, ny, nz = 2, 3, 4
    lattice = generate_cubic_lattice(nx, ny, nz, 5.0, 1.0)
    assert len(lattice.nodes) == (nx + 1) * (ny + 1) * (nz + 1)
    expected_struts = (
        nx * (ny + 1) * (nz + 1)
        + (nx + 1) * ny * (nz + 1)
        + (nx + 1) * (ny + 1) * nz
    )
    assert len(lattice.struts) == expected_struts


def test_total_length_of_a_single_cell():
    lattice = generate_cubic_lattice(1, 1, 1, 10.0, 2.0)
    assert total_strut_length(lattice) == pytest.approx(120.0)


@pytest.mark.parametrize(
    "nx, ny, nz, cell_size, diameter",
    [(0, 1, 1, 10.0, 2.0), (1, 1, 1, -5.0, 2.0), (1, 1, 1, 10.0, 0.0)],
)
def test_invalid_parameters_raise_value_error(nx, ny, nz, cell_size, diameter):
    with pytest.raises(ValueError):
        generate_cubic_lattice(nx, ny, nz, cell_size, diameter)