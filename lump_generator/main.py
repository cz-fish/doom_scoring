#!/usr/bin/env python3

from Parser import Parser, Actor, State
from ActorFilter import ActorFilter
from RewardGenerator import RewardGenerator
from DecorateGenerator import DecorateGenerator
import sys

class FileReader:
    def readLump(self, fileName):
        with open(fileName, 'rt') as f:
            return [l for l in f.readlines()]

def dump(actors):
    with open('all_actors.txt', 'wt') as f:
        for a in actors:
            print("{}: {} replaces {}".format(a.ActorName, a.ParentName, a.Replaces), file=f)
            for s in a.States:
                print("  '{}': {} lines".format(s.Name, len(s.Lines)), file=f)
                #for l in s.Lines:
                #    print("    " + l, file=f)

def main():
    fileReader = FileReader()
    parser = Parser(fileReader, "DECORATE")
    try:
        dec = parser.parse()
    except Exception as e:
        print("Parsing error: {}".format(e))
        for trace in parser.getTraceback():
            print("  in {} on line {}".format(trace[0], trace[1]))
        sys.exit(1)

    ##
    #dump(parser.actors)
    ##

    aFilter = ActorFilter()
    statesToReward = aFilter.findStatesToReward(parser.actors)

    ##
    #dump(scoredStates)
    ##

    reward = RewardGenerator()
    for actor in statesToReward:
        for state in actor.States:
            reward.addPointReward(actor, state)

    # TODO: write the modified scoredStates in DECORATE format
    decorateGenerator = DecorateGenerator("output")
    decorateGenerator.saveDecorate(statesToReward)

if __name__ == '__main__':
    main()

