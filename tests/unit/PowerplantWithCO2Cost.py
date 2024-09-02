from core.production_plan import Fuels, PowerplantWithCO2Cost


def test_powerplantwithc02cost_cost_per_MWh_for_gasfired_type():
    fuels = Fuels(13.4, 50.8, 20, 60)
    powerplant = PowerplantWithCO2Cost(
        "gasfiredbig1", "gasfired", 0.53, 100, 460, fuels
    )
    assert powerplant.cost_per_MWh == 13.4 / 0.53 + 0.3 * fuels.co2
