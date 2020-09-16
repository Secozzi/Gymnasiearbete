from math import ceil


class GridMenu:
    def __init__(self):
        self.menu = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        self.apps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.counter = 0

    def scroll_up(self):
        if self.counter > 0:
            print(f"Can scroll up {self.counter} steps")

    def scroll_down(self):
        if self.counter < ceil((len(self.apps) - 8) / 4):
            print(f"Can scroll down {ceil((len(self.apps) - 8) / 4)} steps")

    def __repr__(self):
        return str(self.menu)


grid = GridMenu()
grid.scroll_down()
print(grid)
