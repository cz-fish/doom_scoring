from Actor import Actor, State

PointsItem = "Points"

class RewardGenerator:
    def __init__(self):
        self.Constants = set()
        self.Items = [PointsItem]

    _ignoreStates = {
         'death.avoid',
         'death.killme',
         'death.taunt',
         'death.tear',
         'death.throwable',
         'death2',
         'death.shotgun',
         'death.shotgunontheface',
         'deathjump',
         'deathmirror',
         'deathnoguts',
         'deathremovearm',
         'death.cutless',
         'pain.avoid',
         'pain.killme',
         'pain.taunt',
         'painak2',
         'xdeathrare'}

    _doomActors = {
            'arachnotron',
            'archvile',
            'baronofhell',
            'bossbrain',
            'cacodemon',
            'chaingunguy',
            'commanderkeen',
            'cyberdemon',
            'demon',
            'doomimp',
            'explosivebarrel',
            'fatso',
            'hellknight',
            'lostsoul',
            'marinebfg',
            'marineberserk',
            'marinechaingun',
            'marinechainsaw',
            'marinefist',
            'marinepistol',
            'marineplasma',
            'marinerailgun',
            'marinerocket',
            'marinessg',
            'marineshotgun',
            'painelemental',
            'revenant',
            'scriptedmarine',
            'shotgunguy',
            'spectre',
            'spidermastermind',
            'wolfensteinss',
            'zombieman'
            }

    _extraActors = set()

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
        # BrutalDoom introduces great many new shootable actors. We want to add
        # points only to those that represent the original Doom monsters (plus any
        # defined extraActors that we might be interested in)
        if not actor.ActorName.lower() in self._doomActors \
           and (not actor.ActorName.lower() in self._extraActors) \
           and (not actor.Replaces \
                or actor.Replaces.lower() not in self._doomActors):
            return None

        if actor.Replaces:
            constName = actor.Replaces
        else:
            constName = actor.ActorName

        selectedStates = []
        for s in actor.GetStates():
            lowerName = s.Name.lower()
            if lowerName in self._ignoreStates:
                continue

            if lowerName.startswith('death.fatality'):
                self._addPointReward(s, self._generateConstName(constName, "Fatality"))
            elif lowerName.startswith('death'):
                self._addPointReward(s, self._generateConstName(constName, "Death"))
            elif lowerName.startswith('xdeath'):
                self._addPointReward(s, self._generateConstName(constName, "SplatterDeath"))
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

