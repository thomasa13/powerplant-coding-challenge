from core.production_plan import Fuels
from pytest import raises


def test_fuels_constructor_missing_gas_raises_error():
    with raises(ValueError):
        Fuels(None, 1, 1, 1)


def test_fuels_constructor_missing_kerosine_raises_error():
    with raises(ValueError):
        Fuels(1, None, 1, 1)


def test_fuels_constructor_missing_co2_raises_error():
    with raises(ValueError):
        Fuels(1, 1, None, 1)


def test_fuels_constructor_missing_wind_raises_error():
    with raises(ValueError):
        Fuels(1, 1, 1, None)


def test_fuels_constructor_invalid_gas_raises_error():
    with raises(ValueError):
        Fuels(-1, 1, 1, 1)


def test_fuels_constructor_invalid_kerosine_raises_error():
    with raises(ValueError):
        Fuels(1, -1, 1, 1)


def test_fuels_constructor_invalid_co2_raises_error():
    with raises(ValueError):
        Fuels(1, 1, -1, 1)


def test_fuels_constructor_invalid_wind_raises_error():
    with raises(ValueError):
        Fuels(1, 1, 1, -1)


def test_fuels_constructor_excessive_wind_raises_error():
    with raises(ValueError):
        Fuels(1, 1, 1, 101)


def test_fuels_constructor_sets_proper_gas():
    assert Fuels(10, 1, 1, 1).gas == 10


def test_fuels_constructor_sets_proper_kerosine():
    assert Fuels(1, 10, 1, 1).kerosine == 10


def test_fuels_constructor_sets_proper_co2():
    assert Fuels(1, 1, 10, 1).co2 == 10


def test_fuels_constructor_sets_proper_wind():
    assert Fuels(1, 1, 1, 10).wind == 10
