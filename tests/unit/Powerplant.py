from core.production_plan import Fuels, Powerplant
from pytest import raises


def test_powerplant_constructor_missing_name_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant(None, "gasfired", 0.53, 100, 460, fuels)


def test_powerplant_constructor_missing_type_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", None, 0.53, 100, 460, fuels)


def test_powerplant_constructor_missing_efficiency_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", None, 100, 460, fuels)


def test_powerplant_constructor_missing_pmin_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, None, 460, fuels)


def test_powerplant_constructor_missing_pmax_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, None, fuels)


def test_powerplant_constructor_missing_fuels_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, None)


def test_powerplant_constructor_invalid_name_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant(1, "gasfired", 0.53, 100, 460, fuels)


def test_powerplant_constructor_invalid_type_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", 1, 0.53, 100, 460, fuels)


def test_powerplant_constructor_invalid_efficiency_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", "0.53", 100, 460, fuels)


def test_powerplant_constructor_invalid_pmin_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, "100", 460, fuels)


def test_powerplant_constructor_invalid_pmax_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, "460", fuels)


def test_powerplant_constructor_invalid_fuels_raises_error():
    with raises(ValueError):
        fuels = Fuels(13.4, 50.8, 20, 60)
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, {})


def test_powerplant_constructor_sets_proper_name():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert (
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).name
        == "gasfiredbig1"
    )


def test_powerplant_constructor_sets_proper_type():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert (
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).type == "gasfired"
    )


def test_powerplant_constructor_sets_proper_efficiency():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert (
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).efficiency == 0.53
    )


def test_powerplant_constructor_sets_proper_pmin():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).pmin == 100


def test_powerplant_constructor_sets_proper_pmin_for_windturbine():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert Powerplant(
        "windturbine", "windturbine", 0.53, 100, 460, fuels
    ).pmin == round(100 * fuels.wind / 100, 1)


def test_powerplant_constructor_sets_proper_pmax():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).pmax == 460


def test_powerplant_constructor_sets_proper_pmax_for_windturbine():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert Powerplant(
        "windturbine", "windturbine", 0.53, 100, 460, fuels
    ).pmax == round(460 * fuels.wind / 100, 1)


def test_powerplant_constructor_sets_proper_fuels():
    fuels = Fuels(13.4, 50.8, 20, 60)
    assert Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels).fuels == fuels


def test_powerplant_cost_per_MWh_for_gasfired_type():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplant = Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels)
    assert powerplant.cost_per_MWh == 13.4 / 0.53


def test_powerplant_cost_per_MWh_for_turbojet_type():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplant = Powerplant("turbojet", "turbojet", 0.53, 100, 460, fuels)
    assert powerplant.cost_per_MWh == 50.8 / 0.53


def test_powerplant_cost_per_MWh_for_windturbine_type():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplant = Powerplant("windturbine", "windturbine", 0.53, 100, 460, fuels)
    assert powerplant.cost_per_MWh == 0
