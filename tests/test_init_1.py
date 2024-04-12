import numpy as np
import pytest


def test_init_1():
    import ELATE


def test_init_2():
    import ELATE
    from ELATE import refdata

    # Load from string
    x = ELATE.Elastic(refdata.examples_3D['FAU'])
    assert isinstance(x, ELATE.Elastic)

    # 6 x 6 matrix
    x = ELATE.Elastic('[[10, 2, 2, 0, 0, 0], [2, 10, 2, 0, 0, 0], [2, 2, 10, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 5]]')
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    x = ELATE.Elastic([[10, 2, 2, 0, 0, 0], [2, 10, 2, 0, 0, 0], [2, 2, 10, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 5]])
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    x = ELATE.Elastic(np.array([[10, 2, 2, 0, 0, 0], [2, 10, 2, 0, 0, 0], [2, 2, 10, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 5]]))
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    # Upper triangular
    x = ELATE.Elastic('[[10, 2, 2, 0, 0, 0], [10, 2, 0, 0, 0], [10, 0, 0, 0], [5, 0, 0], [5, 0], [5]]')
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    x = ELATE.Elastic([[10, 2, 2, 0, 0, 0], [10, 2, 0, 0, 0], [10, 0, 0, 0], [5, 0, 0], [5, 0], [5]])
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    # Lower triangular
    x = ELATE.Elastic('[[10], [2, 10], [2, 2, 10], [0, 0, 0, 5], [0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 5]]')
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)

    x = ELATE.Elastic([[10], [2, 10], [2, 2, 10], [0, 0, 0, 5], [0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 5]])
    assert isinstance(x, ELATE.Elastic)
    assert np.all(x.eigenvalues() > 0)


def test_init_3():
    import ELATE

    with pytest.raises(ValueError):
        ELATE.Elastic([])
    with pytest.raises(ValueError):
        ELATE.Elastic([[]])
    with pytest.raises(ValueError):
        ELATE.Elastic("")
    with pytest.raises(ValueError):
        ELATE.Elastic("1 2 3 4 5 6")
    with pytest.raises(ValueError):
        ELATE.Elastic("1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n")
    with pytest.raises(ValueError):
        ELATE.Elastic("1 1 1 1 1 1\nfoo 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n1 1 1 1 1 1\n")
    with pytest.raises(ValueError):
        ELATE.Elastic(np.array([[10, 2, 2, 0, 0, 0], [2, 10, 2, 0, 0, 0], [2, 2, 10, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 5, 0]]))
    with pytest.raises(ValueError):
        ELATE.Elastic(np.array([[10, 2, 2, 0, 0], [2, 10, 2, 0, 0], [2, 2, 10, 0, 0], [0, 0, 0, 5, 0], [0, 0, 0, 0, 5]]))
