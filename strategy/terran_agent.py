from strategy.agent import Agent as A
import unit.terran_unit as T
from unit.units import Army


class DummyTerran(A):

    def __init__(self, diff=5):
        A.__init__(self)
        self.army_nums = 5
        self.building_nums = 5
        self.difficulty = diff

    def step_auto(self, verbose=False):
        if self.env.all_steps % 5 == 1:
            self.add_unit(T.Marine(), 1)
            if self.env.all_steps >= 15 and self.difficulty >= 3:
                self.add_unit(T.Marine(), 1)
            if self.env.all_steps >= 25 and self.difficulty >= 5:
                self.add_unit(T.Marine(), 1)
            if self.env.all_steps >= 35 and self.difficulty >= 7:
                self.add_unit(T.Marine(), 2)

        if self.military_num() > 50:
            self.env.army[self.player_id].order = Army.Order.ATTACK
        else:
            self.env.army[self.player_id].order = Army.Order.DEFEND

    def set_diff(self, diff):
        self.difficulty = diff

    def reset(self, pos):
        super().reset(pos)
        self.get_power()
        self.army_nums = 5
        self.building_nums = 5

    def get_power(self):
        self.add_unit(T.Marine(), 5)
        self.add_building(T.Commandcenter(), 1)
        self.add_building(T.Supplydepot(), 5)
        self.add_building(T.Barracks(), 2)
