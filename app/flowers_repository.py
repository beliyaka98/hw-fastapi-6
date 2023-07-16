from attrs import define


@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []

    def add_flower(self, name, count, cost):
        flower = Flower(name, count, cost, self.get_next_id())
        self.flowers.append(flower)
    def get_next_id(self):
        return len(self.flowers) + 1
