class Constants:
    def __init__(self, constants):
        self.constants = constants
    
    def __getitem__(self, idx):
        return self.constants[idx]
    
    def __setitem__(self, idx, val):
        self.constants[idx] = val
