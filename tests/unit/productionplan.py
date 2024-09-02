from core.production_plan import (
    Fuels,
    Powerplant,
    PowerplantWithCO2Cost,
    NotEnoughPowerError,
    set_powerplant_production_for_load,
)
from pytest import raises


def test_productionplan_with_regular_dataset():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplants = [
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
        Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
        Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
        Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(480, powerplants)
    assert powerplants[0].p == 368.4
    assert powerplants[1].p == 0.0
    assert powerplants[2].p == 0.0
    assert powerplants[3].p == 0.0
    assert powerplants[4].p == 90.0
    assert powerplants[5].p == 21.6


def test_productionplan_with_no_wind():
    fuels = Fuels(13.4, 50.8, 20, 0)
    powerplants = [
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
        Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
        Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
        Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(480, powerplants)
    assert powerplants[0].p == 380
    assert powerplants[1].p == 100
    assert powerplants[2].p == 0.0
    assert powerplants[3].p == 0.0
    assert powerplants[4].p == 0.0
    assert powerplants[5].p == 0.0


def test_productionplan_with_high_load():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplants = [
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
        Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
        Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
        Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(910, powerplants)
    assert powerplants[0].p == 460.0
    assert powerplants[1].p == 338.4
    assert powerplants[2].p == 0.0
    assert powerplants[3].p == 0.0
    assert powerplants[4].p == 90.0
    assert powerplants[5].p == 21.6


def test_productionplan_with_no_load():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplants = [
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
        Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
        Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
        Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(0, powerplants)
    assert powerplants[0].p == 0.0
    assert powerplants[1].p == 0.0
    assert powerplants[2].p == 0.0
    assert powerplants[3].p == 0.0
    assert powerplants[4].p == 0.0
    assert powerplants[5].p == 0.0


def test_productionplan_with_max_load():
    fuels = Fuels(13.4, 50.8, 20, 50)
    powerplants = [
        Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
        Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
        Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
        Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(1239, powerplants)
    assert powerplants[0].p == 460
    assert powerplants[1].p == 460
    assert powerplants[2].p == 210
    assert powerplants[3].p == 16
    assert powerplants[4].p == 75
    assert powerplants[5].p == 18


def test_productionplan_with_impossibly_high_load():
    with raises(NotEnoughPowerError):
        fuels = Fuels(13.4, 50.8, 20, 50)
        powerplants = [
            Powerplant("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
            Powerplant("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
            Powerplant("gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels),
            Powerplant("tj1", "turbojet", 0.3, 0, 16, fuels),
            Powerplant("windpark1", "windturbine", 1, 0, 150, fuels),
            Powerplant("windpark2", "windturbine", 1, 0, 36, fuels),
        ]
        set_powerplant_production_for_load(1240, powerplants)


def test_productionplan_with_regular_dataset_and_co2_cost():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplants = [
        PowerplantWithCO2Cost("gasfiredbig1", "gasfired", 0.53, 100, 460, fuels),
        PowerplantWithCO2Cost("gasfiredbig2", "gasfired", 0.53, 100, 460, fuels),
        PowerplantWithCO2Cost(
            "gasfiredsomewhatsmaller", "gasfired", 0.37, 40, 210, fuels
        ),
        PowerplantWithCO2Cost("tj1", "turbojet", 0.3, 0, 16, fuels),
        PowerplantWithCO2Cost("windpark1", "windturbine", 1, 0, 150, fuels),
        PowerplantWithCO2Cost("windpark2", "windturbine", 1, 0, 36, fuels),
    ]
    set_powerplant_production_for_load(480, powerplants)
    assert powerplants[0].p == 368.4
    assert powerplants[1].p == 0.0
    assert powerplants[2].p == 0.0
    assert powerplants[3].p == 0.0
    assert powerplants[4].p == 90.0
    assert powerplants[5].p == 21.6


# Todo: tests specifically changing results because of co2 costs
