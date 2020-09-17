from math import ceil


class GridMenu:
    def __init__(self):
        self.menu = ("a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3")
        self.apps = ("a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "c1", "c2")
        #self.apps = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        self.counter = 0

    def scroll_up(self):
        if self.counter > 0:
            new_menu = []
            start = (self.counter - 1) * 4
            to_insert = list(self.apps[start:start + 4])

            new_menu += to_insert
            new_menu += self.menu[0:4]
            self.menu = tuple(new_menu)
            self.counter -= 1

    def scroll_down(self):
        step = ceil((len(self.apps) - 8) / 4)
        if self.counter < step:
            new_menu = []
            next_item = 8 + 4 * self.counter
            to_insert = list(self.apps[next_item:next_item + 4])

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu += self.menu[4:9]
            new_menu += to_insert
            self.menu = tuple(new_menu)
            self.counter += 1

    def __repr__(self):
        return str(self.menu)
