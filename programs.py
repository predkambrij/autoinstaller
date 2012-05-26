#!/usr/bin/python

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put
from fabric.contrib.console import confirm
from fabric.context_managers import show
from fabric.api import env

# import superior
from abscomp import AbsComp


class Programs(AbsComp):
    def __init__(self):
        pass

    def run(self):
        while True:
            case = AbsComp.getCountSection()

            if case == 0:
                if not self.psevdoFunction(0): return False

            elif case == 1:
                if not self.psevdoFunction(1, confirm=1): return False

            elif case == 2:
                if not self.psevdoFunction(2, confirm=1, printstack=1): return False

            else:
                # everything went file - end of cases
                # or -1 as endStatus request)
                break

            AbsComp.countUpSection()

        print "End of programs setup"
        return True


    def psevdoFunction(self, n, confirm=0, printstack=0):
        print "Entered into psevdo method",n
        run("echo \"Entered into psevdo method %d\"" % n)
        
        if confirm:
            return AbsComp.continouePrompt(printstack = printstack)
        else:
            return True


