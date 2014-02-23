#!/usr/bin/env python3

from Parser import Parser, Actor, State
import sys

class FileReader:
    def readLump(self, fileName):
        with open(fileName, 'rt') as f:
            return [l for l in f.readlines()]

def main():
    fileReader = FileReader()
    parser = Parser(fileReader, "DECORATE")
    try:
        dec = parser.parse()
    except Exception as e:
        print("Parsing error: {}".format(e))
        #print(sys.exc_info())
        for trace in parser.getTraceback():
            print("  in {} on line {}".format(trace[0], trace[1]))
        sys.exit(1)

    for actor in parser.actors:
        print ("Actor '{}', {} states".format(actor.ActorName, len(actor.States)))

if __name__ == '__main__':
    main()

