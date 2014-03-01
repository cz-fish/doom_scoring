class State:
    def __init__(self, stateName, lines = None):
        self.Name = stateName
        if lines:
            self.Lines = lines
        else:
            self.Lines = []

    def __str__(self):
        return "<State {}: {} lines>".format(self.Name, len(self.Lines))

    def __repr__(self):
        return str(self)

class Actor:
    def __init__(self, actorName, parentName, replaces):
        self.ActorName = actorName
        self.ParentName = parentName
        self.Replaces = replaces
        self._Shootable = False
        self._States = []
        self._Parent = None

    def SetShootable(self):
        self._Shootable = True

    def AddState(self, state):
        self._States += [state]

    def GetLastState(self):
        return self._States[-1]

    def HasOwnStates(self):
        return len(self._States) > 0

    def IsShootable(self):
        if not self._Parent:
            return self._Shootable
        return self._Shootable or self._Parent.IsShootable()

    def GetStates(self):
        if not self._Parent:
            return self._States
        stateMap = {s.Name: s.Lines for s in self._Parent.GetStates()}
        for s in self._States:
            stateMap[s.Name] = s.Lines
        return [State(name, lines) for name, lines in stateMap.items()]

    def LinkToParent(self, actorMap):
        if self.ParentName and self.ParentName in actorMap:
            self._Parent = actorMap[self.ParentName]

    def __str__(self):
        return "<Actor {}({}) replaces {}, {}shootable>".format(
                self.ActorName,
                self.ParentName,
                self.Replaces,
                ['not',''][self.IsShootable()])

    def __repr__(self):
        return str(self)

