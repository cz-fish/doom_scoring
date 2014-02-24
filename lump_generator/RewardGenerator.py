from Parser import Actor, State

class RewardGenerator:
    def addPointReward(self, actor, state):
        # FIXME
        pointReward = 5
        state.Lines = ["""TNT1 A 0 A_GiveToTarget("Points", {})""".format(pointReward)] + state.Lines

