class HashedString:

    def __init__(self, hash=0, string=''):
        self.hash = hash
        self.string = string

    def __str__(self):
        return self.string


class UnHashedString:

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string
