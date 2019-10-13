class FlexibleList(list):

    def __update_size(self, ind):
        if ind >= len(self):
            self.extend([0] * (ind - len(self) + 1))

    def __getitem__(self, ind):
        self.__update_size(ind)
        return super().__getitem__(ind)

    def __setitem__(self, ind, value):
        self.__update_size(ind)
        return super().__setitem__(ind, value)
