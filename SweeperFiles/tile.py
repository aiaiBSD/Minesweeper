class Tile:
    def __init__(self, isMine, bombNumber):
        self.mine = isMine
        self.number = bombNumber
        self.expand = False

    def getMine(self):
        return self.mine

    def getNumber(self):
        return self.number

    def getExpand(self):
        return self.expand

    def changeMine(self, change):
        self.mine = change

    def changeNumber(self, change):
        self.number = change

    def changeExpand(self, change):
        self.expand = change