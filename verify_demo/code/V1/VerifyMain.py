#!/usr/bin/python

#find the percentiles
#matlab -nodesktop -nosplash -nodisplay -r "percent_tile;quit;" >& out

import os, time, calendar, datetime, sys
from changeto_testlocation import change_to_test_location, locate_exe
from get_id import get_id
import operator

# Code runs in the current directory and uses relative path names
# Writes its result in "./REPORT"

def main():
    global root
    global tests

    root = os.getcwd()

    print 'Tarfile verify, running in directory: '
    print root
    print ''

    #for each submission:
    #1. make a tmp dir
    #2. cp the tar ball to the dir
    #3. extract and the tar ball
    #4. locate the makefile or the executable
    #5. ready to run with the executable

    result = {}

    for submission in os.listdir('./'):
        result_temp = {}

        print '==> testing',submission

        if os.path.isdir(submission):
            continue

        change_to_test_location(submission)

        name, id = get_id()

        tmp = locate_exe(submission)

        #print '\n=======', 'finished', submission, '=======\n'


        #clean up everything that was created during testing
        os.chdir(root)
        fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
        folder = submission.split('.', 1)[0]
        fixed_folder = fixed_submission.split('.', 1)[0]
        os.system('rm ' + fixed_folder + ' -rf')

        print '\n---------------------------------------------------------\n'

    return

if __name__ == "__main__":
    main()
