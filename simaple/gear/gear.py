from pydantic import BaseModel

from simaple.core.base import Stat
from simaple.gear.gear_type import GearType


class Gear(BaseModel):
    id: int
    stat: Stat
    name: str
    type: GearType
    req_level: int
    scroll_chance: int
    boss_reward: bool
    superior_eqp: bool
    req_job: int = 0

    def is_weapon(self) -> bool:
        return GearType.is_weapon(self.type)

    def is_left_weapon(self) -> bool:
        return GearType.is_left_weapon(self.type)

    def is_sub_weapon(self) -> bool:
        return GearType.is_sub_weapon(self.type)

    def is_double_hand_weapon(self) -> bool:
        return GearType.is_double_hand_weapon(self.type)

    def is_armor(self) -> bool:
        return GearType.is_armor(self.type)

    def is_accessory(self) -> bool:
        return GearType.is_accessory(self.type)

    def is_mechanic_gear(self) -> bool:
        return GearType.is_mechanic_gear(self.type)

    def is_dragon_gear(self) -> bool:
        return GearType.is_dragon_gear(self.type)

    def show(self) -> str:
        job_string = (
            "["
            + ("] [").join(
                [(" V " if self.req_job & (1 << i) != 0 else "   ") for i in range(5)]
            )
            + "]"
        )
        output = f"""
        ===================================
        name: {self.name}
        type: {self.type.name} (type number {self.type})
        req_level: {self.req_level}
                 [WAR] [MAG] [ARC] [THF] [PIR]
        req_job: {job_string}
        ===================================
        Basis Stats

        STR: {self.stat.STR}
        DEX: {self.stat.DEX}
        INT: {self.stat.INT}
        LUK: {self.stat.LUK}
        
        MaxHP: {self.stat.MHP}
        MaxMP: {self.stat.MMP}

        ATT: {self.stat.attack_power}
        MAT: {self.stat.magic_attack}

        ===================================
        """
        return output
