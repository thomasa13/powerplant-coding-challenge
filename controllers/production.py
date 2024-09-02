from flask import Blueprint
from flask import request
from core.production_plan import (
    Fuels,
    PowerplantWithCO2Cost,
    NotEnoughPowerError,
    set_powerplant_production_for_load,
)

production_controller = Blueprint(__name__.split(".")[-1], __name__)


@production_controller.route("/productionplan", methods=["POST"])
def production_plan():
    if not isinstance(request.json, dict):
        return "Invalid or missing json body. Must be an object", 400
    if not isinstance(request.json.get("load"), (int, float)):
        return 'Invalid or missing property "load" in body. Must be a number', 400
    if not isinstance(request.json.get("fuels"), dict):
        return 'Invalid or missing property "fuels" in body. Must be an object', 400
    if not isinstance(request.json.get("powerplants"), list):
        return (
            'Invalid or missing property "powerplants" in body. Must be an array of objects',
            400,
        )
    if not isinstance(request.json["fuels"].get("gas(euro/MWh)"), (int, float)):
        return (
            'Invalid or missing properties "gas(euro/MWh)" in fuels. Must be a number',
            400,
        )
    if not isinstance(request.json["fuels"].get("kerosine(euro/MWh)"), (int, float)):
        return (
            'Invalid or missing properties "gas(euro/MWh)" in fuels. Must be a number',
            400,
        )
    if not isinstance(request.json["fuels"].get("co2(euro/ton)"), (int, float)):
        return (
            'Invalid or missing properties "gas(euro/MWh)" in fuels. Must be a number',
            400,
        )
    if not isinstance(request.json["fuels"].get("wind(%)"), (int, float)):
        return (
            'Invalid or missing properties "gas(euro/MWh)" in fuels. Must be a number',
            400,
        )

    try:
        fuels = Fuels(
            request.json["fuels"].get("gas(euro/MWh)"),
            request.json["fuels"].get("kerosine(euro/MWh)"),
            request.json["fuels"].get("co2(euro/ton)"),
            request.json["fuels"].get("wind(%)"),
        )
        powerplants = list(
            map(
                lambda x: PowerplantWithCO2Cost(
                    x.get("name"),
                    x.get("type"),
                    x.get("efficiency"),
                    x.get("pmin"),
                    x.get("pmax"),
                    fuels,
                ),
                request.json["powerplants"],
            )
        )
        set_powerplant_production_for_load(request.json["load"], powerplants)
        return [{"name": x.name, "p": x.p} for x in powerplants]
    except (ValueError, NotEnoughPowerError) as e:
        return e, 400
