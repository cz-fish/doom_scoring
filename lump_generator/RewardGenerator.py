from Parser import Actor, State

pointsItem = "Points"

class RewardGenerator:
    def __init__(self):
        self.Constants = []
        self.Items = [pointsItem]

    def addPointReward(self, actor, state):
        constantName = self._generateConstName(actor.ActorName, state.Name)
        self.Constants += [constantName]
        state.Lines = ["""TNT1 A 0 A_GiveToTarget("{}", {})""".format(pointsItem, constantName)] + state.Lines

    def _generateConstName(self, actorName, stateName):
        if stateName == 'XDeath':
            stateName = 'SplatterDeath'
        return self._normalizeConstName("points{}{}".format(actorName, stateName))

    def _normalizeConstName(self, constName):
        # TODO: make sure that constName is a valid identifier.
        #       Actor name and state name might contain invalid characters
        return constName
