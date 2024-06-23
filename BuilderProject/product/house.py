class House:
    def __init__(self):
        self.foundation = None
        self.structure = None
        self.roof = None
        self.interior = None

    def show(self):
        return {
            "Foundation": self.foundation,
            "Structure": self.structure,
            "Roof": self.roof,
            "Interior": self.interior
        }
