from math import ceil


class GridMenu:
    def __init__(self):
        self.menu = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        self.apps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.counter = 0

    def scroll_up(self):
        if self.counter > 0:
            new_menu = []
            start = (self.counter - 1) * 4
            to_insert = self.apps[start:start + 4]

            new_menu.append(to_insert)
            new_menu.append(self.menu[0])
            self.menu = new_menu
            self.counter -= 1

    def scroll_down(self):
        step = ceil((len(self.apps) - 8) / 4)
        if self.counter < step:
            new_menu = []
            next_item = 8+4*self.counter
            to_insert = self.apps[next_item:next_item+4]

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu.append(self.menu[1])
            new_menu.append(to_insert)
            self.menu = new_menu
            self.counter += 1

    def __repr__(self):
        return str(self.menu)