class Player:

    def __init__(self, id, kills):
        self.__id = id
        self.__kills = kills

    @property
    def id(self):
        return self.__id

    @property
    def kills(self):
        return self.__kills