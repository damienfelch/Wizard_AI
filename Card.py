class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.suit == 'Wizard' or self.suit == 'Jester':
            return f"{self.suit}"
        return f"{self.value} of {self.suit}"
