from enum import Enum


class Queue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def first_item(self):
        # bacause we use pop as newest, so index is -1 not 0
        return self.items[-1]

    def size(self):
        return len(self.items)


class Unit:

    def __init__(self):
        self.mineral_price = 0
        self.gas_price = 0
        self.build_time = 0

        self.hp = 0
        self.armor = 0
        self.attribute = []

        self.attack = 0
        self.multi_hit = 1
        self.range = 0
        self.dps = 0

        self.front = None
        self.pos = [0, 0]
        self.size = 0
        self.progress = 0

    def __hash__(self):
        return hash((self.hp, self.armor, self.attack, self.range, self.mineral_price, self.gas_price))

    def __eq__(self, other):
        return (self.hp, self.armor, self.attack, self.range, self.mineral_price, self.gas_price) == \
            (other.hp, other.range, other.attack, other.range, other.mineral_price, other.gas_price)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class Building(Unit):

    def __init__(self):
        Unit.__init__(self)
        self.food_supply = 0


class Creature(Unit):

    def __init__(self):
        Unit.__init__(self)
        self.movement = 0
        self.food_used = 0
        self.bonus_attack = {}


class Army():

    class Order(Enum):
        NOTHING = 0
        ATTACK = 1
        MOVE = 2
        DEFEND = 3

    def __init__(self, player_id):
        self.player_id = player_id
        self.order = self.Order.NOTHING
        self.list = {}
        self.pos = -1

    def __str__(self):
        return str(self.player_id) + ', ' + str(self.order) + ', ' + str(self.pos)
