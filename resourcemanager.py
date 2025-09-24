
class ResourceManager:
    def __init__(self):
        self.database ={}
    def set_key(self, key, data):
        self.database[str(key)] = data
    def get_key(self, key):
        if key in self.database:
            return self.database[str(key)]
        else:
            return None;