import time
from unit.units import Army


class BattleField():

    def __init__(self, red_agent=None, blue_agent=None, field=None, max_steps=100):
        self.red_agent = red_agent
        self.blue_agent = blue_agent
        self.field = field
        self.max_steps = max_steps

    def get_damage(self, army):
        attack = 0
        damage = 0
        for key, value in army.items():
            unit_type = key
            unit = unit_type()
            attack += unit.attack * value
            damage += unit.dps * (1 + unit.range / 15) * value

        if attack != 0:
            attack /= sum(army.values())

        return attack, damage

    def get_equivalent_hp(self, army, attack):
        all_hp = 0
        for key, value in army.items():
            unit_type = key
            unit = unit_type()
            all_hp += unit.getEquivalentHP(attack) * value

        return all_hp

    def battle(self, verbose=False):
        red_army = self.red_agent.military_force()
        blue_army = self.blue_agent.military_force()

        red_attack, red_damage = self.get_damage(red_army)
        blue_attack, blue_damage = self.get_damage(blue_army)

        red_all_hp = self.get_equivalent_hp(red_army, blue_attack)
        blue_all_hp = self.get_equivalent_hp(blue_army, red_attack)

        red_remain_hp = red_all_hp - blue_damage
        if verbose:
            print(red_remain_hp)

        blue_remain_hp = blue_all_hp - red_damage
        if verbose:
            print(blue_remain_hp)
            print(self.blue_agent.building_hp())

        if blue_remain_hp < 0 and self.field == self.blue_agent.pos:
            self.blue_agent.under_attack(-blue_remain_hp)

        if red_remain_hp < 0 and self.field == self.red_agent.pos:
            self.red_agent.under_attack(-red_remain_hp)

        if verbose:
            print(self.blue_agent.building_hp())

        self.red_agent.reset_military(red_remain_hp)
        self.blue_agent.reset_military(blue_remain_hp)

        red_army = self.red_agent.military_force()
        blue_army = self.blue_agent.military_force()


class SimulatePlatform():

    def __init__(self, red_agent=None, blue_agent=None, distance=5, max_steps=1):
        self.red_agent = red_agent
        self.blue_agent = blue_agent

        self.distance = distance
        self.red_pos = 0
        self.blue_pos = distance - 1
        self.max_steps = max_steps

        self.army = [Army(0), Army(1)]
        self.win_index = -1
        self.all_steps = 0
        self.is_end = False

    def reset(self):
        self.army = [Army(0), Army(1)]
        self.win_index = -1
        self.all_steps = 0
        self.is_end = False

        self.red_agent.reset(self.red_pos)
        self.blue_agent.reset(self.blue_pos)

    def init(self):
        self.red_agent.init(self, player_id=0, pos=self.red_pos)
        self.blue_agent.init(self, player_id=1, pos=self.blue_pos)

    def simulate(self, verbose=False):
        for i in range(self.max_steps):
            self.red_agent.step_auto(verbose)
            self.blue_agent.step_auto(False)

            if verbose:
                time.sleep(1)

            if self.is_end == True:
                break

            self.battle_execute()
            self.all_steps += 1

            if self.blue_agent.building_hp() < 0:
                self.win_index = self.red_agent.player_id
                self.is_end = True
            elif self.red_agent.building_hp() < 0:
                self.win_index = self.blue_agent.player_id
                self.is_end = True
            elif i == self.max_steps - 2:
                self.is_end = True

    def battle_execute(self):
        army_0 = self.army[0]
        army_1 = self.army[1]
        combat_max_steps = 1

        if army_0.pos == army_1.pos:
            bf = BattleField(red_agent=self.red_agent, blue_agent=self.blue_agent, field=army_0.pos)
            for i in range(combat_max_steps):
                bf.battle(False)
        else:
            if army_0.order == Army.Order.ATTACK:
                army_0.pos = min(army_0.pos + 1, self.distance - 1)
            elif army_0.order == Army.Order.DEFEND:
                army_0.pos = max(army_0.pos - 1, 0)

            if army_1.order == Army.Order.ATTACK:
                army_1.pos = max(army_1.pos - 1, 0)
            elif army_1.order == Army.Order.DEFEND:
                army_1.pos = min(army_1.pos + 1, self.distance - 1)
