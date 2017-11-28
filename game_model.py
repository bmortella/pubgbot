class Game:

    def __init__(self, winners, total):
        self.__winners = winners
        self.__total = total

    @property
    def winners(self):
        return self.__winners

    @property
    def total(self):
        return self.__total