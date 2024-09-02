class NotEnoughPowerError(Exception):
    pass


class Fuels:
    def __init__(self, gas: float, kerosine: float, co2: float, wind: float):
        if not isinstance(gas, (int, float)) or gas < 0:
            raise ValueError(
                f'Invalid or missing value "{gas}" for property "gas" of fuels. Must be a number superior or equal to 0'
            )
        self.gas = gas

        if not isinstance(kerosine, (int, float)) or kerosine < 0:
            raise ValueError(
                f'Invalid or missing value "{kerosine}" for property "kerosine" of fuels. Must be a number superior or equal to 0'
            )
        self.kerosine = kerosine

        if not isinstance(co2, (int, float)) or co2 < 0:
            raise ValueError(
                f'Invalid or missing value "{co2}" for property "co2" of fuels. Must be a number superior or equal to 0'
            )
        self.co2 = co2

        if not isinstance(wind, (int, float)) or wind < 0 or wind > 100:
            raise ValueError(
                f'Invalid or missing value "{wind}" for property "wind" of fuels. Must be a number between 0 and 100'
            )
        self.wind = wind


class Powerplant:
    def __init__(
        self,
        name: str,
        type: str,
        efficiency: float,
        pmin: float,
        pmax: float,
        fuels: Fuels,
    ):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError(
                f'Invalid or missing value "{efficiency}" for property "efficiency" of powerplant "{name}". Must be a number between 0 and 1'
            )
        self.name = name

        if type not in ["gasfired", "turbojet", "windturbine"]:
            raise ValueError(
                f'Invalid or missing value "{type}" for property "type" of powerplant "{name}". Must be one of: "gasfired", "turbojet", "windturbine"'
            )
        self.type = type

        if not isinstance(efficiency, (int, float)) or efficiency < 0 or efficiency > 1:
            raise ValueError(
                f'Invalid or missing value "{efficiency}" for property "efficiency" of powerplant "{name}". Must be a number between 0 and 1'
            )
        self.efficiency = efficiency

        if not isinstance(pmin, (int, float)) or pmin < 0:
            raise ValueError(
                f'Invalid or missing value "{pmin}" for property "pmin" of powerplant "{name}". Must be a number superior to 0'
            )
        if not isinstance(pmax, (int, float)) or pmax < 0 or pmax < pmin:
            raise ValueError(
                f'Invalid or missing value "{pmax}" for property "pmax" of powerplant "{name}". Must be a number superior to 0 and superior or equal to pmin'
            )
        if type == "windturbine":
            pmin = round(pmin * fuels.wind / 100, 1)
            pmax = round(pmax * fuels.wind / 100, 1)
        self.pmin = pmin
        self.pmax = pmax

        if not isinstance(fuels, Fuels):
            raise ValueError(
                f'Invalid or missing property "fuels" of powerplant "{name}". Must be instance of Fuels'
            )
        self.fuels = fuels
        self.p = 0.0

    @property
    def is_valid(self):
        return (
            self.pmax > 0
            and self.pmax >= self.pmin
            and not (self.type == "windturbine" and self.fuels.wind == 0)
        )

    @property
    def cost_per_MWh(self):
        if self.type == "gasfired":
            return self.fuels.gas / self.efficiency
        if self.type == "turbojet":
            return self.fuels.kerosine / self.efficiency
        if self.type == "windturbine":
            return 0


class PowerplantWithCO2Cost(Powerplant):
    @property
    def cost_per_MWh(self):
        if self.type == "gasfired":
            return super().cost_per_MWh + 0.3 * self.fuels.co2
        return super().cost_per_MWh


# Getting the most cost efficient combination requires two criteria :
# - Prioritizing powerplants per cost of production
# - Reducing the loss caused from pmin forcing us to reduce usage of more cost efficient powerplants
def set_powerplant_production_for_load(load: int, powerplants: list[Powerplant]):
    powerplants = [x for x in powerplants]
    powerplants.sort(key=lambda x: x.cost_per_MWh)

    while load > sum([powerplant.p for powerplant in powerplants]):
        missing_load = round(load - sum([x.p for x in powerplants]), 1)
        active_powerplants_per_cost = [x for x in powerplants if x.p > 0 and x.is_valid]
        active_powerplants_per_cost.reverse()

        # Choose best powerplant and apply modification to all necessary productions
        best_powerplant_to_add = get_next_best_powerplant_to_add(
            missing_load, powerplants
        )

        if missing_load >= best_powerplant_to_add.pmin:
            best_powerplant_to_add.p = min(missing_load, best_powerplant_to_add.pmax)
        else:
            load_reduction_to_distribute = best_powerplant_to_add.pmin - missing_load
            active_powerplants_per_cost = [x for x in powerplants if x.p > 0]
            active_powerplants_per_cost.reverse()
            best_powerplant_to_add.p = best_powerplant_to_add.pmin

            # Reduce the active powerplants to compensate for the new powerplant's pmin
            for active_powerplant in active_powerplants_per_cost:
                MWh_to_reduce = min(
                    load_reduction_to_distribute,
                    active_powerplant.pmax - active_powerplant.pmin,
                )
                load_reduction_to_distribute -= MWh_to_reduce
                active_powerplant.p -= MWh_to_reduce


def get_next_best_powerplant_to_add(missing_load, powerplants):
    cost_to_add_powerplant = []
    active_powerplants_per_cost = [x for x in powerplants if x.p > 0 and x.is_valid]
    active_powerplants_per_cost.reverse()
    inactive_powerplants = [x for x in powerplants if x.p == 0 and x.is_valid]
    if len(inactive_powerplants) == 0:
        raise NotEnoughPowerError(
            "Impossible with such powerplants, not enough max power"
        )

    # Calculate cost per MWh to add this powerplant in the calculation
    # Includes cost of reducing of active powerplants to satisfy pmin when necessary
    # Result set in cost_to_add_powerplant list
    for powerplant in inactive_powerplants:
        new_powerplant_load = max(
            powerplant.pmin,
            min(missing_load, powerplant.pmax),
        )
        load_reduction_to_distribute = (
            new_powerplant_load - missing_load
            if new_powerplant_load > missing_load
            else 0
        )
        load_reduction_profit = 0

        # Traverse the active powerplants starting by the most expensive to reduce their load to satisfy pmin of current powerplant if necessary
        for active_powerplant in active_powerplants_per_cost:
            MWh_to_reduce = min(
                load_reduction_to_distribute,
                active_powerplant.pmax - active_powerplant.pmin,
            )
            load_reduction_profit += active_powerplant.cost_per_MWh * MWh_to_reduce
            load_reduction_to_distribute -= MWh_to_reduce

        cost_to_add_powerplant.append(
            (powerplant.cost_per_MWh * new_powerplant_load - load_reduction_profit)
            / (new_powerplant_load if new_powerplant_load > 0 else 1)
        )

    return inactive_powerplants[
        cost_to_add_powerplant.index(min(cost_to_add_powerplant))
    ]
