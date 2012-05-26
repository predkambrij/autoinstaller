#!/usr/bin/python

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
from fabric.context_managers import show
from fabric.api import env

# import config. Values are as attributes in object
from conf import conf_class

# rewrite env variable from config file
env = conf_class.env

#include modules
from environment import Environment
from programs import Programs

# class of god
from abscomp import AbsComp

class Deploy(AbsComp):

    def __init__(self):
        pass
        # no return here

    def psevdoFunction(self, n, confirm=0, printstack=0):
        print "Entered into psevdo method",n
        run("echo \"Entered into psevdo method %d\"" % n)
        
        if confirm:
            return AbsComp.continouePrompt(printstack = printstack)
        else:
            return True

    def run(self):
        # as static variable to AbsComp will set current status
        AbsComp.startState()
        
        # assumptions: every case can be rerunable
        
        # first section
        firstSection = AbsComp.newSection()

        while True:
            case = AbsComp.getCountSection()

            if case == 0:
                if not self.psevdoFunction(0,confirm=1,printstack=1): break

                # write the commands | standard fabric commands
                run("echo \"Let's get started!\"")
                #put(AbsComp.old_disk+"/opt/shots", "/opt/shots")
                # ...
                # ...

            elif case == 1:
                # write subblock
                status = AbsComp.newSection()

                flagEnd=0
                # setup environment
                while True:
                    subcase = AbsComp.getCountSection()

                    if subcase == 0:
                        if AbsComp.oper_sys == "ubuntu":
                            print "Your operating system is ubuntu, so do this"
                            if not self.psevdoFunction(0):
                                flagEnd=1
                                break
                        elif AbsComp.oper_sys == "debian":
                            print "Your operating system is debian, so do this" 
                            if not self.psevdoFunction(0):
                                flagEnd=1
                                break
                        else:
                            print "Unrecognized operating system"
                            AbsComp.continouePrompt(printstack = 1)

                    elif subcase == 1:
                        if not self.psevdoFunction(1, confirm=1):
                            flagEnd=1
                            break

                    elif subcase == 2:
                        if not self.psevdoFunction(2, confirm=1, printstack=1):
                            flagEnd=1
                            break

                    else:
                        # everything went fine - end of cases
                        # or -1 as endStatus request)
                        # end of subblock
                        AbsComp.endSection(status)
                        break

                    AbsComp.countUpSection()

                # if subsection didn't completed successfully break also external loop
                if flagEnd == 1:
                    break


            elif case == 2:
                # write subblock in separated file

                status = AbsComp.newSection()

                # install programs
                p = Programs()
                ret = p.run()
                if ret != True:
                    break

                # end of subblock
                AbsComp.endSection(status)

            else:
                # everything went file - end of cases
                # or -1 as endStatus request)
                # end of first section
                AbsComp.endSection(firstSection)
                break

            AbsComp.countUpSection()


        # save current status to database if requested
        AbsComp.endState()
        
        print "Finish! Autoinstaller didn't crashed!"
        return True


#################################################################

# run fabric
def deploy():
    # do everything
    d = Deploy()
    d.run()
    return True

def prerequirements():
    AbsComp.prerequirements(indeploy=0)

def help():
    print "Ensure that your server and target satisfy prerequirements:"
    print "fab prerequirements"
    print "For deploy :"
    print "fab deploy"
