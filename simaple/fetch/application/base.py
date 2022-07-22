from loguru import logger

from simaple.fetch.element import (
    MapleItemListElement,
    character_promise,
    item_promise,
    maple_item_list_promise,
    pet_list_promise,
)
from simaple.fetch.token import TokenRepository


class Application:
    ...


class KMSFetchApplication(Application):
    def run(self, name: str):
        token_repository = TokenRepository()
        token = token_repository.get(name)

        item = maple_item_list_promise().then(
            {
                idx: item_promise()
                for idx in set(
                    MapleItemListElement.expected_normal_names()
                    + MapleItemListElement.expected_arcane_names()
                )
            }
        )

        character = character_promise()

        pet = pet_list_promise().then({idx: item_promise() for idx in range(3)})

        logger.info(item.resolve("", token))
        logger.info(character.resolve("", token))
        logger.info(pet.resolve("", token))
