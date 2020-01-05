from unit.units import Building
from unit.units import Creature


class ZergBuilding(Building):

    def __init__(self):
        super().__init__()

    def getEquivalentHP(self, attack):
        if attack == 0:
            return self.hp
        else:
            return self.hp * attack / max(attack - self.armor, 1)


class ZergCreature(Creature):

    def __init__(self):
        super().__init__()

    def getEquivalentHP(self, attack):
        if attack == 0:
            return self.hp
        else:
            return self.hp * attack / max(attack - self.armor, 1)


class Hatchery(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()
        self.larva = 0

    def specialization(self):
        self.mineral_price = 300
        self.gas_price = 0
        self.build_time = 71
        self.food_supply = 14

        self.hp = 1500
        self.attack = 0

        self.armor = 1
        self.range = 0

    def createLarva(self):
        self.larva += 1


class Extractor(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 25
        self.gas_price = 0
        self.build_time = 21
        self.food_supply = 0

        self.hp = 500
        self.armor = 1

        self.attack = 0
        self.range = 0


class SpawningPool(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 200
        self.gas_price = 0
        self.build_time = 46
        self.food_supply = 0

        self.hp = 1000
        self.armor = 1

        self.attack = 0
        self.range = 0


class EvolutionChamber(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 75
        self.gas_price = 0
        self.build_time = 25
        self.food_supply = 0

        self.hp = 750
        self.armor = 1

        self.attack = 0
        self.range = 0


class SpineCrawler(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 0
        self.build_time = 36
        self.food_supply = 0

        self.hp = 300
        self.armor = 2

        self.attack = 25
        self.range = 7
        self.dps = 18.9


class SporeCrawler(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 75
        self.gas_price = 0
        self.build_time = 21
        self.food_supply = 0

        self.hp = 400
        self.armor = 1

        self.attack = 15
        self.range = 7
        self.dps = 24.6


class RoachWarren(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 39
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class BanelingNest(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 50
        self.build_time = 43
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class Lair(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 100
        self.build_time = 57
        self.food_supply = 14

        self.hp = 2000
        self.armor = 1

        self.attack = 0
        self.range = 0

    def createLarva(self):
        self.larva += 1


class HydraliskDen(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 100
        self.build_time = 29
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class LurkerDen(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 86
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class InfestationPit(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 100
        self.build_time = 36
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class Spire(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 200
        self.gas_price = 200
        self.build_time = 71
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class NydusNetwork(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 200
        self.build_time = 36
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class NydusWorm(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 100
        self.build_time = 14
        self.food_supply = 0

        self.hp = 200
        self.armor = 1

        self.attack = 0
        self.range = 0


class Hive(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 200
        self.gas_price = 150
        self.build_time = 71
        self.food_supply = 14

        self.hp = 2500
        self.armor = 1

        self.attack = 0
        self.range = 0

    def createLarva(self):
        self.larva += 1


class UltraliskCavern(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 200
        self.build_time = 46
        self.food_supply = 0

        self.hp = 850
        self.armor = 1

        self.attack = 0
        self.range = 0


class GreaterSpire(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 150
        self.build_time = 71
        self.food_supply = 0

        self.hp = 1000
        self.armor = 1

        self.attack = 0
        self.range = 0


class CreepTumor(ZergBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 11
        self.food_supply = 0

        self.hp = 50
        self.armor = 0

        self.attack = 0
        self.range = 0


class Larva(ZergCreature):
    # created by Hatchery

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 11
        self.food_used = 0

        self.hp = 25
        self.armor = 10

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 0.79


class Drone(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 0
        self.build_time = 12
        self.food_used = 1

        self.hp = 40
        self.armor = 0

        self.attack = 5
        self.range = 0
        self.dps = 4.7
        self.movement = 3.94


class Queen(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 36
        self.food_used = 2

        self.hp = 175
        self.armor = 1

        self.attack = 8
        self.range = 0
        self.dps = 11.3
        self.movement = 1.31


class Zergling(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 0
        self.build_time = 17
        self.food_used = 0.5

        self.hp = 35
        self.armor = 0

        self.attack = 5
        self.range = 0
        self.dps = 10
        self.movement = 4.13


class Baneling(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 25
        self.gas_price = 25
        self.build_time = 14
        self.food_used = 0.5

        self.hp = 30
        self.armor = 0

        self.attack = 20
        self.range = 0
        self.dps = 0
        self.movement = 3.5


class Roach(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 75
        self.gas_price = 25
        self.build_time = 19
        self.food_used = 2

        self.hp = 145
        self.armor = 1

        self.attack = 16
        self.range = 4
        self.dps = 11.2
        self.movement = 3.15


class Ravager(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 25
        self.gas_price = 75
        self.build_time = 9
        self.food_used = 3

        self.hp = 120
        self.armor = 1

        self.attack = 16
        self.range = 6
        self.dps = 14
        self.movement = 3.85


class Hydralisk(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 50
        self.build_time = 24
        self.food_used = 2

        self.hp = 90
        self.armor = 0

        self.attack = 12
        self.range = 5
        self.dps = 22.2
        self.movement = 3.15


class Lurker(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 100
        self.build_time = 18
        self.food_used = 3

        self.hp = 200
        self.armor = 1

        self.attack = 20
        self.range = 9
        self.dps = 13.99
        self.movement = 4.13


class Infestor(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 150
        self.build_time = 36
        self.food_used = 2

        self.hp = 90
        self.armor = 0

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 3.15


class InfestedTerran(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 3
        self.food_used = 0

        self.hp = 50
        self.armor = 0

        self.attack = 6
        self.range = 5
        self.dps = 10
        self.movement = 1.31


class SwarmHost(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 75
        self.build_time = 29
        self.food_used = 3

        self.hp = 160
        self.armor = 1

        self.attack = 0
        self.range = 0
        self.dps = 23.25
        self.movement = 3.15


class Locust(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 3
        self.food_used = 0

        self.hp = 50
        self.armor = 0

        self.attack = 10
        self.range = 6
        self.dps = 23.25
        self.movement = 2.62


class Ultralisk(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 300
        self.gas_price = 200
        self.build_time = 39
        self.food_used = 6

        self.hp = 500
        self.armor = 2

        self.attack = 35
        self.range = 1
        self.dps = 57.4
        self.movement = 4.13


class Overlord(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 0
        self.build_time = 18
        self.food_supply = 8

        self.hp = 200
        self.armor = 0

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 0.902


class Overseer(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 50
        self.build_time = 12
        self.food_used = 0

        self.hp = 200
        self.armor = 1

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 2.62


class Changeling(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 1
        self.food_used = 0

        self.hp = 5
        self.armor = 0

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 3.15


class Mutalisk(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 100
        self.build_time = 24
        self.food_used = 2

        self.hp = 120
        self.armor = 0

        self.attack = 9
        self.range = 3
        self.dps = 8.3
        self.movement = 5.6


class Corruptor(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 100
        self.build_time = 29
        self.food_used = 2

        self.hp = 200
        self.armor = 2

        self.attack = 14
        self.range = 6
        self.dps = 10.3
        self.movement = 4.725


class Viper(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 200
        self.build_time = 29
        self.food_used = 3

        self.hp = 150
        self.armor = 1

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 4.13


class BroodLord(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 24
        self.food_used = 4

        self.hp = 225
        self.armor = 1

        self.attack = 20
        self.range = 10
        self.dps = 11.2
        self.movement = 1.97


class Broodling(ZergCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 1
        self.food_used = 0

        self.hp = 30
        self.armor = 0

        self.attack = 4
        self.range = 0
        self.dps = 8.7
        self.movement = 5.37
