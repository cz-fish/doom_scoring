# Simplified parser of DECORATE lumps.
# This is not aiming to be a complete parser; we only need specific
# small parts of the file, we don't need to understand it all.
# Of course, without a proper lexical analyzer, the parsing is quite
# fragile.

import re
from Actor import State, Actor

includePattern = re.compile(r'^#include\W+([^ \t]+)', flags=re.IGNORECASE)
actorPattern = re.compile(r'^actor\W+([^: \t]+)(?:\W*:\W*(\w+)\W*(?:replaces\W*(\w+))?)?', flags=re.IGNORECASE)
shootablePattern = re.compile(r'(?:\bmonster\b)|(?:\+ISMONSTER\b)|(?:\+SHOOTABLE\b)', flags=re.IGNORECASE)
statesPattern = re.compile(r'^states', flags=re.IGNORECASE)
stateLabelPattern = re.compile(r'^([^: \t]+):')

class ParserException(Exception):
    pass


class Parser:
    def __init__(self, fileReader, rootFile):
        self.fileReader = fileReader
        self.contentsStack = [self.fileReader.readLump(rootFile)]
        self.fileStack = [rootFile]
        self.filePos = [0]
        self.actors = []
        self.actorMap = {}

    def parse(self):
        insideComment = False
        braceLevel = 0
        actorBraceLevel = -1
        statesBraceLevel = -1
        for l in self.contentsStack[-1]:
            self.filePos[-1] += 1
            l, insideComment = self._stripComments(l, insideComment)
            l = l.strip()
            if (l == ''):
                continue

            for hunk, increment in self._splitByBraces(l):
                hunk = hunk.strip()

                # #include
                m = includePattern.match(hunk)
                if m:
                    if braceLevel != 0:
                        raise ParserException("Include nested in {} block. We don't support that.")
                    self._include(m)

                # Actor
                m = actorPattern.match(hunk)
                if m:
                    if braceLevel != 0:
                        raise ParserException("Actor nested in {} block. We don't support that.")
                    if actorBraceLevel != -1:
                        raise ParserException("Actor nested inside actor.")
                    self._actor(m)
                    actorBraceLevel = braceLevel + 1

                # Monster
                m = shootablePattern.search(hunk)
                if m:
                    if braceLevel == actorBraceLevel:
                        self.actors[-1].SetShootable()

                # States
                m = statesPattern.match(hunk)
                if m:
                    if braceLevel == actorBraceLevel and statesBraceLevel == -1:
                        statesBraceLevel = braceLevel + 1
                    
                # state label
                m = stateLabelPattern.match(hunk)
                if m:
                    if braceLevel == statesBraceLevel:
                        self._stateHeader(m)
                elif braceLevel == statesBraceLevel and hunk != '':
                    self._stateAction(hunk)

                braceLevel += increment
                if braceLevel < 0:
                    raise ParserException("Unbalanced braces: Too many closing braces")
                if increment < 0 and braceLevel < statesBraceLevel:
                    # We have passed the closing brace of the States {} block, so we are no longer in the block
                    statesBraceLevel = -1
                if increment < 0 and braceLevel < actorBraceLevel:
                    # We have passed the closing brace of the Actor {} block, so we are no longer in the block
                    actorBraceLevel = -1

        if braceLevel > 0:
            raise ParserException("Unbalanced braces: Too many opening braces")
        self.contentsStack = self.contentsStack[:-1]
        self.fileStack = self.fileStack[:-1]
        self.filePos = self.filePos[:-1]

    def getTraceback(self):
        return [tb for tb in zip(self.fileStack, self.filePos)]

    def resolveParentLinks(self):
        for actor in self.actors:
            actor.LinkToParent(self.actorMap)

    def _include(self, match):
        fileName = match.group(1)
        self.fileStack += [fileName]
        self.filePos += [0]
        self.contentsStack += [self.fileReader.readLump(fileName)]
        self.parse()

    def _actor(self, match):
        actorName = match.group(1)
        parentName = match.group(2)
        replaces = match.group(3)
        newActor = Actor(actorName, parentName, replaces)
        self.actors += [newActor]
        self.actorMap[actorName] = newActor

    def _stateHeader(self, match):
        stateName = match.group(1)
        self.actors[-1].AddState(State(stateName))

    def _stateAction(self, line):
        if not self.actors[-1].HasOwnStates():
            self.actors[-1].AddState(State(""))
        self.actors[-1].GetLastState().Lines += [line]


    def _stripComments(self, line, insideComment):
        commentStart1 = line.find('//')
        commentStart2 = line.find('/*')
        commentEnd2 = line.find('*/')
        first = min([-1]+[i for i in [commentStart1, commentStart2, commentEnd2] if i != -1])
        if first == -1:
            # No comment mark of any sort on the current line
            if insideComment:
                return ('', insideComment)
            else:
                return (line, insideComment)
        elif first == commentStart1:
            if insideComment:
                return self._stripComments(line[commentStart1 + 2:], insideComment)
            else:
                return (line[:commentStart1], False)
        elif first == commentStart2:
            if insideComment:
                raise ParseException("Nested comment blocks")
            else:
                trailer, insideComment = self._stripComments(line[commentStart2 + 2:], True)
                return (line[:commentStart2] + trailer, insideComment)
        elif first == commentEnd2:
            if insideComment:
                return self._stripComments(line[commentEnd2 + 2:], False)
            else:
                raise ParseException("End of comment block without a matching start")

    def _splitByBraces(self, line):
        pos = 0
        for i in range(len(line)):
            if line[i] == '{':
                yield (line[pos:i], 1)
                pos = i + 1
            elif line[i] == '}':
                yield (line[pos:i], -1)
                pos = i + 1
        yield (line[pos:], 0)

