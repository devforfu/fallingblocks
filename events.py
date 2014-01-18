class Event:
    pass

class TickEvent(Event):
    pass

class DummyEvent(Event):
    """ Is used by MouseClick agent, which actually has not to plan anything. """
    pass

class QuitEvent(Event):
    pass

class CellClickEvent(Event):
    def __init__(self, x, y):
        self.pos = self.x, self.y = x, y

class RequestDecisionEvent(Event):
    def __init__(self, index, game):
        self.index = index
        self.game = game

class ChosenDecisionEvent(Event):
    def __init__(self, action):
        self.action = action

class DrawEvent(Event):
    def __init__(self, x, y, figure):
        self.figure = figure
        self.x, self.y = x, y

class WinnerEvent(Event):
    def __init__(self, winner):
        self.winner = winner

class DrawEndEvent(Event):
    pass

class EventManager:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def registerListener(self, subj):
        self.listeners[subj] = True

    def unregisterListener(self, subj):
        if subj in self.listeners:
            del self.listeners[subj]

    def broadcast(self, event):
        for listener in self.listeners:
            if hasattr(listener, 'notify'):
                listener.notify(event)