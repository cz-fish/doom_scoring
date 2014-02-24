import os
import os.path
from Parser import Actor, State

class DecorateGenerator:
    def __init__(self, path):
        self.path = path

    def saveDecorate(self, actors):
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
                for s in a.States:
                    print("    {}:".format(s.Name), file = f)
                    for l in s.Lines:
                        print("        " + l, file = f)
                print("    }", file = f)
                print("}", file=f)

        self._saveMasterFile(includes)

    def _saveMasterFile(self, includes):
        with open(os.path.join(self.path, 'DECORATE'), 'wt') as f:
            for i in includes:
                print("#include {}".format(i), file = f)

            print("", file = f)
            print("ACTOR Points: Inventory", file = f)
            print("{", file = f)
            print("}", file = f)


