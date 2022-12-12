import re
from abc import ABCMeta, abstractmethod

import bs4
import pydantic
import re


class NumberString:
    @classmethod
    def number_string_to_int(cls, number_string: str) -> int:
        return int(cls.sanitize(number_string))

    @classmethod
    def is_number(cls, number_string: str) -> bool:
        return str.isdigit(cls.sanitize(number_string))

    @classmethod
    def sanitize(cls, number_string: str) -> str:
        return number_string.strip().replace(" ", "").replace(",", "").replace("%", "")


class CharacterPropertyExtractor(pydantic.BaseModel, metaclass=ABCMeta):
    @abstractmethod
    def extract(self, soup: bs4.BeautifulSoup):
        ...

    def sanitize(self, result) -> dict:
        sanitized_result = {}
        for k, v in result.items():
            if isinstance(v, str) and NumberString.is_number(v):
                sanitized_result[k] = NumberString.number_string_to_int(v)
            else:
                sanitized_result[k] = v

        return sanitized_result


class CharacterNameExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        name_element = soup.select_one(".char_info_top .char_name span")
        name_regex = re.compile("(.+)님$")
        name = re.search(name_regex, name_element.text).group(1)

        return name


class CharacterLevelExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        level_element = soup.select_one(".char_info_top .char_info dd")
        level_regex = re.compile(r"LV\.([0-9]+)")
        level = int(level_regex.match(level_element.text).group(1))

        return level


class CharacterOverviewExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        objectives = soup.select(".tab01_con_wrap table:nth-of-type(1) tbody td")
        overview_key_list = ("world", "job", "pop", "guild", "meso", "point")

        result = {
            overview_key: entity.text
            for overview_key, entity in zip(overview_key_list, objectives)
        }
        return self.sanitize(result)


class CharacterStatExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        stat_elements = soup.select(".tab01_con_wrap table:nth-of-type(2) tr")[:-2]
        result = {}

        stat_key_matrix = (
            ("damage_factor", "MHP"),
            ("MP", "STR"),
            ("DEX", "INT"),
            ("LUK", "critical_damage"),
            ("boss_damage_multiplier", "ignored_defence"),
            ("immunity", "stance"),
            ("armor", "speed"),
            ("jump", "starforce"),
            ("honor_point", "arcaneforce"),
        )

        for stat_key_tuple, element in zip(stat_key_matrix, stat_elements):
            for stat_key, td_element in zip(stat_key_tuple, element.find_all("td")):
                result[stat_key] = td_element.text

        min_damage_factor, max_damage_factor = result.pop("damage_factor").split("~")
        result["min_damage_factor"] = min_damage_factor
        result["max_damage_factor"] = max_damage_factor

        return self.sanitize(result)


class CharacterAbilityExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        return [
            el.text
            for el in soup.select_one(
                ".tab01_con_wrap table:nth-of-type(2) tr:nth-last-of-type(2) td span"
            ).children
            if isinstance(el, bs4.element.NavigableString)
        ]


class CharacterHyperstatExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        '''
        # STR, DEX, INT, LUK, HP%, MP%, DF/TF/PP/영력, 크확, 크뎀, 방무, 데미지, 보뎀, 일뎀, 내성, 공마, 경험치, 아케인포스
        # 스탯에는 스탯퍼 미적용
        '''

        stat_elements = [
            el.text
            for el in soup.select_one(
                ".tab01_con_wrap table:nth-of-type(2) tr:nth-last-of-type(1) td span"
            ).children
            if isinstance(el, bs4.element.NavigableString)
        ]

        keys = ["STR", "DEX", "INT", "LUK", "HP", "MP", "DF", "PP",
                "critical_rate", "critical_damage", "ignored_defence",
                "damage_multiplier", "boss_damage_multiplier",
                "immunity", "attack_power", "magic_attack", "arcaneforce"]

        regexes = {
            "STR": re.compile('힘 \d+ 증가'),
            "DEX": re.compile('민첩성 \d+ 증가'),
            "INT": re.compile('지력 \d+ 증가'),
            "LUK": re.compile('운 \d+ 증가'),
            "HP": re.compile('최대 HP \d+% 증가'),
            "MP": re.compile('최대 MP \d+% 증가'),
            "DF": re.compile('최대 데몬 포스/타임 포스 \d+ 증가'),
            "PP": re.compile('최대 싸이킥 포인트 \d+ 증가'),
            "critical_rate": re.compile('크리티컬 확률 \d+% 증가'),
            "critical_damage": re.compile('크리티컬 데미지 \d+% 증가'),
            "ignored_defence": re.compile('방어율 무시 \d+% 증가'),
            "damage_multiplier": re.compile('데미지 \d+% 증가'),
            "boss_damage_multiplier": re.compile('보스 몬스터 공격 시 데미지 \d+% 증가'),
            "immunity": re.compile('상태이상 내성 \d+ 증가'),
            "attack_power": re.compile('공격력과 마력 \d+ 증가'),
            "magic_attack": re.compile('공격력과 마력 \d+ 증가'),
            "arcaneforce": re.compile('아케인포스 \d+ 증가'),
        }

        result = {}
        for key in keys:
            for element in stat_elements:
                if regexes[key].match(element):
                    result[key] = float(re.findall("\d+", element)[0])
            # if the key does not exists, set as 0
            if key not in result:
                result[key] = 0.0
        return result


class CharacterTraitExtractor(CharacterPropertyExtractor):
    def extract(self, soup):
        def extract_level(level_text: str) -> int:
            match = re.compile("^Lv. ([0-9]+)").match(level_text)
            if not match:
                return 0

            return int(match.group(1))

        return {
            element.find("h2").text: extract_level(
                element.select_one(".graph_wrap .lv").text
            )
            for element in soup.select(".tab02_con_wrap .dis_center")
        }
