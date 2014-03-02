from Actor import Actor, State

PointsItem = "Points"

class RewardGenerator:
    def __init__(self):
        self.Constants = set()
        self.Items = [PointsItem]

    _ignoreStates = set()
    _ignoreActors = set()

    def valueActors(self, allActors):
        selectedActors = []
        for actor in allActors:
            filteredStates = self._filterSingleActor(actor)
            if filteredStates:
                selectedActors += [Actor(actor.ActorName, actor.ParentName, actor.Replaces)]
                for s in filteredStates:
                    selectedActors[-1].AddState(s)
        # TODO: handle possible duplicates in the selectedActors list
        return selectedActors

    def _filterSingleActor(self, actor):
        if not actor.IsShootable():
            return None

        if actor.ActorName in self._ignoreActors:
            return None

        selectedStates = []
        for s in actor.GetStates():
            lowerName = s.Name.lower()
            if lowerName in self._ignoreStates:
                continue

            if lowerName.startswith('death.fatality'):
                self._addPointReward(s, self._generateConstName(actor.ActorName, "Fatality"))
            elif lowerName.startswith('death'):
                self._addPointReward(s, self._generateConstName(actor.ActorName, "Death"))
            elif lowerName.startswith('xdeath'):
                self._addPointReward(s, self._generateConstName(actor.ActorName, "SplatterDeath"))
            elif lowerName.startswith('pain'):
                self._addPointReward(s, self._generateConstName('', "Pain"))
            else:
                continue

            selectedStates += [s]
        return selectedStates


    def _addPointReward(self, state, constName):
        self.Constants.add(constName)
        state.Lines = ["""TNT1 A 0 A_GiveToTarget("{}", {})""".format(PointsItem, constName),
                       """goto Super::{}""".format(state.Name)]

    def _generateConstName(self, actorName, stateName):
        return self._normalizeConstName("points{}{}".format(actorName, stateName))

    def _normalizeConstName(self, constName):
        # TODO: make sure that constName is a valid identifier.
        #       Actor name and state name might contain invalid characters
        return constName

