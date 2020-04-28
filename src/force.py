class Force:
    def __init__(self, magnitude):
        self.magnitude = magnitude  # Not really magnitude...
        self.x = 0
        self.y = 0
        self.mBackup = magnitude

    def update(self, x, y):
        self.x = x
        self.y = y

    def on(self, b):
        if b:
            self.magnitude = self.mBackup
        else:
            self.magnitude = 0
