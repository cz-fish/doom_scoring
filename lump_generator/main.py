#!/usr/bin/env python3

import sys
import getopt
import os
from Actor import State, Actor
from Parser import Parser
from ActorFilter import ActorFilter
from RewardGenerator import RewardGenerator
from DecorateGenerator import DecorateGenerator

class FileReader:
    def __init__(self, path):
        self.path = path

    def readLump(self, fileName):
        with open(os.path.join(self.path, fileName), 'rt') as f:
            return [l for l in f.readlines()]

def dump(path, actors):
    with open(os.path.join(path, 'all_actors.txt'), 'wt') as f:
        for a in actors:
            print(str(a), file=f)
            for s in a.GetStates():
                print("  " + str(s), file=f)
                #for l in s.Lines:
                #    print("    " + l, file=f)

def PrintHelp():
    print("""Options:
  -h                this help
  -i <path>         input directory (default .)
  -o <path>         output directory (default ./output)""")

def main():
    inputDir = '.'
    outputDir = './output'
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
    for o, a in opts:
        if o == '-h':
            PrintHelp()
            sys.exit()
        elif o == '-i':
            inputDir = a
        elif o == '-o':
            outputDir = a

    fileReader = FileReader(inputDir)
    parser = Parser(fileReader, "DECORATE")
    try:
        dec = parser.parse()
    except Exception as e:
        print("Parsing error: {}".format(e))
        for trace in parser.getTraceback():
            print("  in {} on line {}".format(trace[0], trace[1]))
        sys.exit(1)
    parser.resolveParentLinks()

    ##
    #dump(outputDir, parser.actors)
    ##

    aFilter = ActorFilter()
    actorsForReward = aFilter.findStatesToReward(parser.actors)

    ##
    #dump(outputDir, actorsForReward)
    ##

    reward = RewardGenerator()
    for actor in actorsForReward:
        for state in actor.GetStates():
            reward.addPointReward(actor, state)
    pointConstants = reward.Constants
    rewardItems = reward.Items

    # write the modified scoredStates in DECORATE format
    decorateGenerator = DecorateGenerator(outputDir)
    decorateGenerator.saveDecorate(actorsForReward, pointConstants, rewardItems)

if __name__ == '__main__':
    main()

