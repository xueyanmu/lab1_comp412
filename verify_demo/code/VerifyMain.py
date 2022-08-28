#!/usr/bin/python

import os, time, calendar, datetime, sys
from changeto_testlocation import change_to_test_location, locate_exe
from get_id import get_id
import operator

# Code runs in the current directory and uses relative path names
# It is designed to be invoked by a script that changes the directoory
# into the directory holding the code and then invoked this program.
#
# Writes its result in "./REPORT"

def main():
    global TARFILE
    global README
    global NAME
    global NETID
    global EXECUTABLE

    current_dir = os.getcwd()

    print 'Tarfile verifier, running in the directory:'
    print current_dir
    print ''

    # the plan:
    # for each submission:
    # 1. make a tmp dir                    
    # 2. cp the tar ball to the dir
    # 3. extract the tar ball
    # 4. locate the README and extract NAME and NETID
    # 5. locate the makefile, if any, and invoke it
    # 6. locate the executable and check its permissions

    result = {}

    for submission in os.listdir('./'):
        TARFILE = 0
        README = 0
        NAME   = ''
        NETID  = ''
        EXECUTABLE = 0

        print '==> testing',submission

        if os.path.isdir(submission):
            continue
        # 1, 2, & 3 in the plan    
        change_to_test_location(submission)  

        # 4 in the plan
        get_id()                             

        tmp = locate_exe(submission)

        #print '\n=======', 'finished', submission, '=======\n'


        #clean up everything that was created during testing
        os.chdir(current_dir)
        fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
        folder = submission.split('.', 1)[0]
        fixed_folder = fixed_submission.split('.', 1)[0]
        os.system('rm ' + fixed_folder + ' -rf')

        print '\n---------------------------------------------------------\n'

    return

if __name__ == "__main__":
    main()
