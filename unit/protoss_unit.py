from unit.units import Building, Creature, Queue


class ProtossBuilding(Building):

    def __init__(self):
        super().__init__()
        self.shield = 0
        self.shield_armor = 0

    def getEquivalentHP(self, attack):
        if attack == 0:
            return self.hp + self.shield
        else:
            return self.hp * attack / max(attack - self.armor, 1) + \
                self.shield * attack / max(attack - self.shield_armor, 1)


class ProtossCreature(Creature):

    def __init__(self):
        super().__init__()
        self.shield = 0
        self.shield_armor = 0

    def getEquivalentHP(self, attack):
        if attack == 0:
            return self.hp + self.shield
        else:
            return self.hp * attack / max(attack - self.armor, 1) + \
                self.shield * attack / max(attack - self.shield_armor, 1)


# Basic Buildings


class Nexus(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 400
        self.gas_price = 0
        self.build_time = 71
        self.food_supply = 15

        self.hp = 1000
        self.shield = 1000
        self.armor = 1
        self.shield_armor = 0

        self.queue = Queue()


class Pylon(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 0
        self.build_time = 18
        self.food_supply = 8

        self.hp = 200
        self.shield = 200
        self.armor = 1
        self.shield_armor = 0


class Assimilator(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 75
        self.gas_price = 0
        self.build_time = 21

        self.hp = 300
        self.shield = 300
        self.armor = 1
        self.shield_armor = 0


class PhotonCannon(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 29

        self.hp = 150
        self.shield = 150
        self.armor = 1
        self.shield_armor = 0

        self.attack = 20
        self.range = 7
        self.dps = 22.4


class ShieldBattery(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 0
        self.build_time = 29

        self.hp = 150
        self.shield = 150
        self.armor = 1
        self.shield_armor = 0


# Producing Buildings


class Gateway(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 46

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0

        self.max_size = 5
        self.queue = Queue()


class Warpgate(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 7

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0


class RoboticsFacility(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 200
        self.gas_price = 100
        self.build_time = 46

        self.hp = 450
        self.shield = 450
        self.armor = 1
        self.shield_armor = 0


class Stargate(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 43

        self.hp = 600
        self.shield = 600
        self.armor = 1
        self.shield_armor = 0


# Technologic Buildings


class Forge(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 32

        self.hp = 400
        self.shield = 400
        self.armor = 1
        self.shield_armor = 0


class CyberneticsCore(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 36

        self.hp = 550
        self.shield = 550
        self.armor = 1
        self.shield_armor = 0


class TwilightCouncil(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 0
        self.build_time = 36

        self.hp = 550
        self.shield = 550
        self.armor = 1
        self.shield_armor = 0


class TemplarArchives(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 200
        self.build_time = 36

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0


class DarkShrine(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 71

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0


class RoboticsBBay(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 46

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0


class FleetBeacon(ProtossBuilding):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 300
        self.gas_price = 200
        self.build_time = 43

        self.hp = 500
        self.shield = 500
        self.armor = 1
        self.shield_armor = 0


# Worker


class Probe(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 0
        self.build_time = 12
        self.food_used = 1

        self.hp = 20
        self.shield = 20
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['L', 'M']

        self.attack = 5
        self.range = 0
        self.dps = 4.7
        self.movement = 3.94


# Gateway Units


class Zealot(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 0
        self.build_time = 27
        self.food_used = 2

        self.hp = 100
        self.shield = 50
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['L', 'B']

        self.attack = 16
        self.range = 0
        self.dps = 18.6
        self.bonus_attack = {}
        self.movement = 3.15


class Stalker(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 125
        self.gas_price = 50
        self.build_time = 30
        self.food_used = 2

        self.hp = 80
        self.shield = 80
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['A', 'M']

        self.attack = 13
        self.range = 6
        self.dps = 9.7
        self.bonus_attack = {'A': 5}
        self.movement = 4.13


class Sentry(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 100
        self.build_time = 26
        self.food_used = 2

        self.hp = 40
        self.shield = 40
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['L', 'M', 'P']

        self.attack = 6
        self.range = 5
        self.dps = 8.5
        self.movement = 3.15


class Adept(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 100
        self.gas_price = 25
        self.build_time = 27
        self.food_used = 2

        self.hp = 70
        self.shield = 70
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['L', 'B']

        self.attack = 10
        self.range = 4
        self.dps = 6.2
        self.bonus_attack = {'L': 12}
        self.movement = 3.5


class HighTemplar(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 50
        self.gas_price = 150
        self.build_time = 39
        self.food_used = 2

        self.hp = 40
        self.shield = 40
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['L', 'B', 'P']

        self.attack = 4
        self.range = 6
        self.dps = 3.2
        self.movement = 2.62


class DarkTemplar(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 125
        self.gas_price = 125
        self.build_time = 39
        self.food_used = 2

        self.hp = 40
        self.shield = 80
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['L', 'B', 'P']

        self.attack = 45
        self.range = 0
        self.dps = 37.2
        self.movement = 3.94


class Archon(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 9
        self.food_used = 4

        self.hp = 10
        self.shield = 350
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['P', 'Ma']

        self.attack = 25
        self.range = 3
        self.dps = 20
        self.bonus_attack = {'B': 10}
        self.movement = 3.94


# Robotics Facility Units


class Observer(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 25
        self.gas_price = 75
        self.build_time = 21
        self.food_used = 1

        self.hp = 40
        self.shield = 20
        self.armor = 0
        self.shield_armor = 0

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 2.62


class WarpPrism(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 200
        self.gas_price = 0
        self.build_time = 36
        self.food_used = 2

        self.hp = 80
        self.shield = 100
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['A', 'M', 'P']

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 4.13


class Immortal(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 250
        self.gas_price = 100
        self.build_time = 39
        self.food_used = 4

        self.hp = 250
        self.shield = 100
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['A', 'M']

        self.attack = 20
        self.range = 6
        self.dps = 19.2
        self.bonus_attack = {'A': 30}
        self.movement = 3.15


class Colossus(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 300
        self.gas_price = 200
        self.build_time = 54
        self.food_used = 6

        self.hp = 200
        self.shield = 150
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['A', 'M', 'Ma']

        self.attack = 20
        self.range = 7
        self.dps = 18.7
        self.bonus_attack = {'L': 5}
        self.movement = 3.15


class Disruptor(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 36
        self.food_used = 3

        self.hp = 100
        self.shield = 100
        self.armor = 1
        self.shield_armor = 0
        self.attribute = ['A', 'M']

        self.attack = 0
        self.range = 0
        self.dps = 0
        self.movement = 3.15


# Stargate Units


class Phoenix(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 100
        self.build_time = 25
        self.food_used = 2

        self.hp = 120
        self.shield = 60
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['L', 'M']

        self.attack = 10
        self.range = 5
        self.dps = 12.6
        self.bonus_attack = {'L': 5}
        self.movement = 5.95


class VoidRay(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 250
        self.gas_price = 150
        self.build_time = 43
        self.food_used = 4

        self.hp = 150
        self.shield = 100
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['A', 'M']

        self.attack = 6
        self.range = 6
        self.dps = 16.8
        self.bonus_attack = {'A': 4}
        self.movement = 3.5


class Oracle(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 150
        self.gas_price = 150
        self.build_time = 36
        self.food_used = 3

        self.hp = 100
        self.shield = 60
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['L', 'M', 'P']

        self.attack = 15
        self.range = 4
        self.dps = 24.4
        self.bonus_attack = {'L': 7}
        self.movement = 5.6


class Tempest(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 250
        self.gas_price = 175
        self.build_time = 43
        self.food_used = 5

        self.hp = 150
        self.shield = 125
        self.armor = 2
        self.shield_armor = 0
        self.attribute = ['A', 'M', 'Ma']

        self.attack = 40
        self.range = 15
        self.dps = 16.97
        self.bonus_attack = {'Ma': 22}
        self.movement = 3.5


class Carrier(ProtossCreature):

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 350
        self.gas_price = 250
        self.build_time = 64
        self.food_used = 6

        self.hp = 300
        self.shield = 150
        self.armor = 2
        self.shield_armor = 0
        self.attribute = ['A', 'M', 'Ma']

        self.attack = 10
        self.range = 8
        self.dps = 37.8
        self.movement = 2.62


class Interceptor(ProtossCreature):
    # created by Carrier

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 15
        self.gas_price = 0
        self.build_time = 11
        self.food_used = 0

        self.hp = 40
        self.shield = 40
        self.armor = 0
        self.shield_armor = 0
        self.attribute = ['L', 'M']

        self.attack = 10
        self.range = 2
        self.dps = 4.7
        self.movement = 10.5


class Mothership(ProtossCreature):
    # producted by Nexus

    def __init__(self):
        super().__init__()
        self.specialization()

    def specialization(self):
        self.mineral_price = 300
        self.gas_price = 300
        self.build_time = 71
        self.food_used = 8

        self.hp = 350
        self.shield = 350
        self.armor = 2
        self.shield_armor = 0
        self.attribute = ['A', 'M', 'P', 'Ma']

        self.attack = 36
        self.range = 7
        self.dps = 22.8
        self.movement = 2.62
