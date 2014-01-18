class Stack:
    def __init__(self):
        self._data = []
    def push(self, x):
        self._data.append(x)
    def pop(self):
        x = self._data[-1]
        self._data = self._data[:-1]
        return x
    def isEmpty(self, ):
        return len(self._data) == 0
    def clear(self):
        self._data = []

class Queue(Stack):
    def __init__(self):
        super().__init__()
    def pop(self):
        x = self._data[0]
        self._data = self._data[1:]
        return x

class PriorityQueue(Stack):
    def __init__(self, function=lambda x: x, maximize=True):
        super().__init__()
        self.fn = function
        self.maximize = maximize
    def pop(self):
        iteration = max if self.maximize else min
        x = iteration(self._data, key=self.fn)
        self._data.remove(x)
        return x

