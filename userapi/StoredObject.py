class StoredObject:
    def __eq__(self, other):
        return int(self.id) == int(other.id)

    def __ne__(self, other):
        return int(self.id) != int(other.id)

    def __hash__(self):
        return int(self.id)
