#!/usr/bin/python

import os, sys, re

# for save and read last state
import sqlite3

import inspect, traceback

# import config. Values are as attributes in object
from conf import conf_class


class AbsComp:
    files_dir = conf_class.files_dir
    old_disk = conf_class.old_disk
    oper_sys = conf_class.oper_sys
    status = []
    endStatus = []
    depth = -1
    interrupted = 0

    # sections (chain for maintains last status)
    @staticmethod
    def newSection():
        AbsComp.depth += 1

        if AbsComp.depth == len(AbsComp.status):
            AbsComp.status.append(0)
        return AbsComp.status[:AbsComp.depth]

    @staticmethod
    def endSection(firstSection = None):
        if len(AbsComp.status) == 0:
            print "Internal error. AbsComp.endSection was called too much times"
            sys.exit(1)

        del AbsComp.status[-1]
        AbsComp.depth = (len(AbsComp.status) - 1)

        # validate that status before nested section is same then before calling
        if firstSection != None and AbsComp.interrupted == 0:
            if firstSection != AbsComp.status:
                print "Internal error. After nested section is AbsComp.status different then before call"
                print "AbsComp.status before: " + str(repr(firstSection)) + " after: " + str(repr(AbsComp.status))
                sys.exit(1)
            
        return True

    @staticmethod
    def countUpSection():
        # only when program reached end status can continoue with execution
        AbsComp.status[-1] += 1
        return True

    @staticmethod
    def getCountSection():
        # if user requested point where program must stop with execution then stop it
        if AbsComp.status >= AbsComp.endStatus and AbsComp.endStatus != []:
            return -1

        # print debug status
        print "Entering to status:", repr(AbsComp.status[:AbsComp.depth+1])

        # else return current dephest number
        try:
            AbsComp.status[AbsComp.depth]
        except IndexError, e:
            print "Internal error "+repr(e.args)
            print "AbsComp.status " + repr(AbsComp.status)
            print "AbsComp.depth " + str(AbsComp.depth)
            sys.exit(1)
        return AbsComp.status[AbsComp.depth]

    @staticmethod
    def askForStartSession(onlyEnd=0):
        # syntax parseble for list
        p = re.compile(" *\[ *([0-9]+( *, *[0-9]+ *)*)? *\] *")
        # defaults
        start = []
        end = []

        if onlyEnd == 0:
            # get start list
            while True:
                ret = raw_input("Enter start session (blank for begin from start):\nExample for form [2, 3, 2] ")
                ret = ret.strip()

                if ret == "":
                    break

                if p.match(ret) != None:
                    start = eval(ret)
                    break
                else:
                    print "Parse error! Please try again!"

        # get end list
        while True:
            ret = raw_input("Enter end session (blank for end at end):\nExample for form [2, 3, 2] ")
            ret = ret.strip()

            if ret == "":
                break

            if p.match(ret) != None:
                end = eval(ret)
                if start >= end:
                    print "Start must be littler of end! Eg.: [1,1] < [1,2]"
                    print "Please try again! For restart press Ctrl + c"
                    continue
                break
            else:
                print "Parse error! Please try again!"

        if onlyEnd == 0:
            return start, end
        else:
            return end

    # type -> module, function, case
    # case -> number of last successfuly completed operation
    # eg.: module 1 fun 3 case 5
    # ((0, 1), (1, 3), (2, 5))
    # represents .1.3.5
    @staticmethod
    def startState():
        # connect with database
        try:
            con = sqlite3.connect("status.db")
            cur = con.cursor()
        except sqlite3.Error,e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        # create table for saving start status
        cur.execute("CREATE TABLE IF NOT EXISTS status (id INTEGER PRIMARY KEY AUTOINCREMENT, typeno INT, caseno INT)")

        # get AbsComp.status value
        cur.execute("SELECT typeno, caseno FROM status ORDER BY typeno ASC")
        rows = cur.fetchall()

        status = []
        for row in rows:
            status.append(row[1])

        # delete current data (we have it in variable status)
        cur.execute("DELETE FROM status")
        con.commit()

        # close connection
        try:
            con.close()
        except sqlite3.Error,e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        if status == []:
            AbsComp.status, AbsComp.endStatus = AbsComp.askForStartSession(onlyEnd=0)
        else:
            print "Previous session detected!"
            ret = raw_input("Do you want to use that session [y/N] "+str(repr(status))+" : ")
            if ret.lower() == "y":
                AbsComp.status = status
                AbsComp.endStatus = AbsComp.askForStartSession(onlyEnd=1)
            else:
                AbsComp.status, AbsComp.endStatus = AbsComp.askForStartSession()

        print "Autoinstaller ran with status: " + repr(AbsComp.status)
        return True

    @staticmethod
    def endState():
        # connect with database
        try:
            con = sqlite3.connect("status.db")
            cur = con.cursor()
        except sqlite3.Error,e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        # rewrite status variable to database
        for index in range(len(AbsComp.status)):
            # save status value
            cur.execute("INSERT INTO status (typeno, caseno) VALUES (?, ?)", (index, AbsComp.status[index]))
            con.commit()

        print "Autoinstaller exited with status " + repr(AbsComp.status)

        # close connection
        try:
            con.close()
        except sqlite3.Error,e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        return True


    # execution helpers
    #validate that object returned by run() is valid
    @staticmethod
    def errorHandling(x):
        if x.return_code != 0:
            print "Previous command didn't complete successfully"
            return AbsComp.continouePrompt()
        else:
            return True

    # prerequirements of deploy
    @staticmethod
    def prerequirements(indeploy=1):
        print
        print "Prerequirements on server side (side of this script):"
        print "apt-get install sqlite3"
        print "sqlite3 status.db"
        print "sqlite> .exit"
        print
        print "Prerequirements for continoue deploy:"
        print "install debian / ubuntu"
        print "install ssh server (apt-get install openssh-server)"
        print "sshkeygen ..."
        print "cd ~/.ssh"
        print "mv id_rsa.pub authorized_keys"
        print "scp id_rsa to fabric server"
        print "rm id_rsa"
        print
        if indeploy:
            return AbsComp.continouePrompt(printstack = 0)
        else:
            return True

    # if printstack is set then trace will be printed
    # if interrupt is set verification in endSection will be ignored
    @staticmethod
    def continouePrompt(printstack=1, interrupt=1):
        if printstack:
            # prepare stack
            stack = traceback.format_stack(inspect.currentframe())
            newstack = []
            adding = 0
            for frame in stack:
                if adding == 0 and "fabfile.py\"" in frame:
                    adding = 1
                if adding:
                    newstack.append(frame)
            print "Location: ", "\n", "\n".join(newstack[:-1])

        n = raw_input("Continoue? [y/N]:")
        n = n.strip()
        if n.lower()=="y":
            return True
        else:
            if interrupt == 1:
                AbsComp.interrupt = 1
            return False

