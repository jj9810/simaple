from simaple.fetch.element.character import standard_character_element


def test_item_element():
    element = standard_character_element()

    with open("tests/fetch/resources/character.html", encoding="euc-kr") as f:
        html_text = f.read()

    result = element.run(html_text)
    assert result == {
        "name": "생분자",
        "level": 275,
        "overview": {
            "world": "크로아",
            "job": "마법사/아크메이지(불,독)",
            "pop": 1860,
            "guild": "Shiny",
            "meso": 169913574,
            "point": 2735,
        },
        "stat": {
            "min_damage_factor": 104185958,
            "max_damage_factor": 108527036,
            "MHP": 43438,
            "MP": 106562,
            "STR": 5044,
            "DEX": 4535,
            "INT": 52802,
            "LUK": 8138,
            "critical_damage": 75,
            "boss_damage_multiplier": 303,
            "ignored_defence": 96,
            "immunity": 45,
            "stance": 100,
            "armor": 21769,
            "speed": 140,
            "jump": 123,
            "starforce": 345,
            "honor_point": 646603,
            "arcaneforce": 1360,
        },
        "ability": [
            "버프 스킬의 지속 시간 50% 증가",
            "상태 이상에 걸린 대상 공격 시 데미지 7% 증가",
            "크리티컬 확률 20% 증가",
        ],
        "hyperstat": {
            "STR": 0,
            "DEX": 0,
            "INT": 150.0,
            "LUK": 60.0,
            "HP": 0,
            "MP": 0,
            "DF": 0,
            "PP": 0,
            "critical_rate": 13.0,
            "critical_damage": 12.0,
            "ignored_defence": 36.0,
            "damage_multiplier": 36.0,
            "boss_damage_multiplier": 43.0,
            "immunity": 0,
            "attack_power": 18.0,
            "magic_attack": 18.0,
            "arcaneforce": 0,
        },
        "trait": {"카리스마": 100, "통찰력": 100, "의지": 100, "손재주": 100, "감성": 100, "매력": 100},
    }
