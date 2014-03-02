import re

superSearchPattern = re.compile(r'\bSuper::', flags=re.IGNORECASE)

class State:
    def __init__(self, stateName, lines = None):
        self.Name = stateName
        if lines:
            self.Lines = lines
        else:
            self.Lines = []

    def ReplaceSuper(self, substitute):
        """Replaces Super:: with <substitute>:: in all lines"""
        repl = substitute + "::"
        for i in range(len(self.Lines)):
            self.Lines[i] = superSearchPattern.sub(repl, self.Lines[i])

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
        self._SkipSuper = False
        self._States = []
        self._Parent = None

    def SetShootable(self):
        """Marks the actor as shootable.
        Besides monsters, this also applies to barrels and some other special objects."""
        self._Shootable = True

    def SetSkipSuper(self):
        """Makes the actor ignore flags set on its parent actor.
        States are still inherited from the parent, though."""
        self._SkipSuper = True

    def AddState(self, state):
        """Adds a new state to the actor"""
        self._States += [state]

    def GetLastState(self):
        """Returns the last state that was added to the actor.
        Disregards any states inherited from the parent.
        Will raise exception on actors that don't have any states yet."""
        return self._States[-1]

    def HasOwnStates(self):
        """Returns True iff the actor has any states on its own (i.e. not counting any
        states inherited from the parent)."""
        return len(self._States) > 0

    def IsShootable(self):
        """Returns True iff the actor is shootable, or is inherited from a shootable
        actor and doesn't overrule the inheritance by the Skip_Super flag."""
        if not self._Parent or self._SkipSuper:
            return self._Shootable
        return self._Shootable or self._Parent.IsShootable()

    def GetStates(self):
        """Returns all states of the actor in a list in an undefined order.
        This includes states inherited from the parent (with respect to redefinition
        of states in the derived actor)."""
        if not self._Parent:
            return self._States
        stateMap = {s.Name: s.Lines for s in self._Parent.GetStates()}
        for s in self._States:
            stateMap[s.Name] = s.Lines
        return [State(name, lines) for name, lines in stateMap.items()]

    def LinkToParent(self, actorMap):
        """Creates a link between the actor and its parent actor object (if any).
        actorMap is a dictionary that maps actor names to actor objects and this actor
        instance will use it to look up its parent by the name."""
        if self.ParentName and self.ParentName in actorMap:
            self._Parent = actorMap[self.ParentName]

    def FixReferencesToSuper(self):
        """Replaces Super:: with grandparent's name in state actions

        Each actor may call it's parent's state by using the Super::<state> syntax.
        We will be deriving a new actor from the current one and taking over its state
        definitions. If the current actor references its own parent by Super::, the newly
        derived actor would on the othet hand reference the current actor with Super::,
        but what we'd need instead in the derived actor is the parent's parent (something
        like Super::Super::). It can be shortened by using the <GrandparentName>:: syntax.
        
        This method replaces all Super:: references in the actor's states with name of
        this actor's parent."""
        if not self.ParentName:
            return
        for s in self._States:
            s.ReplaceSuper(self.ParentName)

    def __str__(self):
        return "<Actor {}({}) replaces {}, {}shootable>".format(
                self.ActorName,
                self.ParentName,
                self.Replaces,
                ['not ',''][self.IsShootable()])

    def __repr__(self):
        return str(self)

