class HashedString(str):

    def __new__(cls, string='', string_hash=0, *args, **kwargs):
        new_str =  super(HashedString, cls).__new__(cls, string)
        new_str.hash = string_hash
        return new_str

    def __init__(self, string='', string_hash=0):
        self.hash = string_hash


class UnHashedString(str):

    def __new__(cls, string='', *args, **kwargs):
        return super(UnHashedString, cls).__new__(cls, string)
