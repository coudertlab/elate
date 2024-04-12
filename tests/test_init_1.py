import pytest


def test_init_1():
    import ELATE

def test_init_2():
    import ELATE
    from ELATE import refdata

    x = ELATE.Elastic(refdata.examples_3D['FAU'])
    assert isinstance(x, ELATE.Elastic)

