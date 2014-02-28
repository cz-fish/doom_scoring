from Parser import Actor, State

class ActorFilter:
    def findStatesToReward(self, allActors):
        selectedActors = []
        for actor in allActors:
            filteredStates = self._filterSingleActor(actor)
            if filteredStates:
                selectedActors += [Actor(actor.ActorName, actor.ParentName, actor.Replaces)]
                selectedActors[-1].States = filteredStates

        # TODO: handle possible duplicates in the selectedActors list

        return selectedActors

    _interestingStates = ['Death', 'XDeath']

    def _filterSingleActor(self, actor):
        if not actor.Shootable:
            return []

        selectedStates = []
        for s in actor.States:
            if s.Name in self._interestingStates:
                selectedStates += [s]
        return selectedStates

