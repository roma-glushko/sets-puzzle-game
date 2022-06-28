import dataclasses
import random
from collections import defaultdict
from typing import Optional

NUM_OPTIONS_PER_PROPERTY: int = 3
NUM_SETS_TO_GEN: int = 6
NUM_ITEMS_TO_GEN: int = 12
NUM_ITEMS_IN_SET: int = 3

PROPERTIES: tuple[str, ...] = ("symbol", "color", "number", "shading")


@dataclasses.dataclass
class SetItem:
    symbol: int
    color: int
    number: int
    shading: int

    def __repr__(self):
        return f"Set(symb:{self.symbol}, colr: {self.color}, num: {self.number}, shd: {self.shading})"

    def __hash__(self):
        return hash((self.symbol, self.color, self.number, self.shading))

    @classmethod
    def random(cls) -> "SetItem":
        return cls(
            random.randint(1, NUM_OPTIONS_PER_PROPERTY),
            random.randint(1, NUM_OPTIONS_PER_PROPERTY),
            random.randint(1, NUM_OPTIONS_PER_PROPERTY),
            random.randint(1, NUM_OPTIONS_PER_PROPERTY),
        )


GameSet = tuple[SetItem, SetItem, SetItem]


def gen_set_third_item(seeds: set[SetItem]) -> SetItem:
    existing_props: dict[str, set[int]] = defaultdict(set)
    all_options: set[int] = set([i + 1 for i in range(NUM_OPTIONS_PER_PROPERTY)])

    for seed in seeds:
        for prop in PROPERTIES:
            existing_props[prop].add(getattr(seed, prop))

    third_item_props: dict[str, int] = {}

    for prop in PROPERTIES:
        existing_options: set[int] = existing_props[prop]

        if len(existing_options) == 1:
            # Two items have the same prop, then 3rd one should have it as well
            third_item_props[prop] = list(existing_options)[0]
            continue

        # Two items have different prop, then 3rd one should have a different prop as well

        third_item_props[prop] = list(all_options - existing_options)[0]

    return SetItem(**third_item_props)


def gen_set(
    item1: Optional[SetItem] = None, item2: Optional[SetItem] = None
) -> GameSet:
    seed_item1: SetItem = item1 or SetItem.random()
    seed_item2: SetItem = item2 or SetItem.random()
    seed_item3: SetItem = gen_set_third_item({seed_item1, seed_item2})

    return seed_item1, seed_item2, seed_item3


def gen_set_from(existing_items: set[SetItem]) -> GameSet:
    seed_items: list[SetItem] = []

    for _ in range(random.randint(1, 2)):
        seed_items.append(random.choice(list(existing_items)))

    return gen_set(*seed_items)


def validate_set(game_set: GameSet) -> bool:
    pass


def find_sets(
    num_items: int = NUM_ITEMS_TO_GEN, num_sets: int = NUM_SETS_TO_GEN
) -> tuple[list[GameSet], set[SetItem]]:
    game_sets: list[GameSet] = []
    items: set[SetItem] = set()

    if num_sets * NUM_ITEMS_IN_SET < num_items:
        raise RuntimeError(
            f"Number of expected items ({num_items}) contradicts with number of sets ({num_sets})."
            f" Each set has {NUM_OPTIONS_PER_PROPERTY}, "
            f"so you should expect at least {num_sets * NUM_ITEMS_IN_SET} items"
        )

    while len(items) < num_items and len(game_sets) < num_sets:
        # pick all random items to seed the find process. Also, nothing to pick from the existing items
        # otherwise, pick one or two existing items at random and generate a new set with them
        game_set: GameSet = gen_set() if not len(game_sets) else gen_set_from(items)

        game_sets.append(game_set)
        items = items.union(set(game_set))

    if len(items) == num_items:
        return game_sets, items

    # need to add the remaining slots with random items
    while len(items) < num_items:
        items.add(SetItem.random())

    return game_sets, items


if __name__ == "__main__":
    sets, items = find_sets()

    print(f"Sets: {len(sets)}")
    print(f"Unique Items: {len(items)}")

    print("Sets:")
    for game_set in sets:
        print(game_set)

    print("Items:")
    for item in items:
        print(item)
