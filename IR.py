class IR:
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None

    def __getitem__(self, index):

        if isinstance(self.item, int):
            return self.item
        return self.item[index]

    def __setitem__(self, item, value):
        self.item[item] = value

    def __len__(self):
        return len(self.item)