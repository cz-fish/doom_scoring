import os
import os.path
from Actor import Actor, State

# name of the file included from DECORATE that contains constants for point scores
constantsFile = "pointconstants"
# name of the file included from DECORATE that defines actors used for scoring
itemsFileName = "scoringitems"
# suffix added to monster's actor name to differentiate it from its parent
classNameSuffix = "WithReward"
# suffix added to the monster's actor class in the file name
fileNameSuffix = "WR"

class DecorateGenerator:
    def __init__(self, path):
        self.path = path

    def saveDecorate(self, actors, constants, items):
        os.makedirs(self.path, exist_ok=True)
        includes = []
        for a in actors:
            newClass = a.ActorName + "WithReward"
            fileName = a.ActorName + "WR"
            includes += [fileName]
            with open(os.path.join(self.path, fileName), 'wt') as f:
                print("ACTOR {}: {} replaces {}".format(newClass, a.ActorName, a.ActorName), file=f)
                print("{", file=f)
                print("    States", file = f)
                print("    {", file = f)
                for s in a.GetStates():
                    print("    {}:".format(s.Name), file = f)
                    for l in s.Lines:
                        print("        " + l, file = f)
                print("    }", file = f)
                print("}", file=f)

        if items:
            self._saveItems(items)
            includes = [itemsFileName] + includes
        if constants:
            self._saveConstants(constants)
            includes = [constantsFile] + includes
        self._saveMasterFile(includes)

    def _saveItems(self, items):
        with open(os.path.join(self.path, itemsFileName), 'wt') as f:
            for item in items:
                print("", file = f)
                print("ACTOR {}: Inventory".format(item), file = f)
                print("{", file = f)
                print("}", file = f)

    def _saveConstants(self, constants):
        sortedConst = [c for c in constants]
        sortedConst.sort()
        with open(os.path.join(self.path, constantsFile), 'wt') as f:
            for const in sortedConst:
                print("const int {} = 0;".format(const), file = f)

    def _saveMasterFile(self, includes):
        with open(os.path.join(self.path, 'DECORATE'), 'wt') as f:
            for i in includes:
                print("#include {}".format(i), file = f)



