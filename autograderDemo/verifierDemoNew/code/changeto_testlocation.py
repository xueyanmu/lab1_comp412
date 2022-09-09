#!/usr/bin/python

import os

#submission is the name of a given tar ball
def change_to_test_location(submission):
    print '\nChecking the tar archive file'

    #in case of "frag1 frag2 (frag3) frag4's"
    fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
    folder = submission.split('.', 1)[0]
    fixed_folder = fixed_submission.split('.', 1)[0]

    # if folder exists, remove it to restart what we are doing
    if os.path.exists(folder):
        cmd = 'rm -rf ' + fixed_folder 
        os.system(cmd)

    # make dir and cp
    #print '======== ' + submission
    #print '======== ' + folder
    os.makedirs(folder)
    cmd = 'cp ' + fixed_submission + ' ' + fixed_folder
    os.system(cmd)

    # change dir
    os.chdir(folder)
    cmd = 'echo "\nSubmission does not look like a tar archive file.\n"'
    # unzip or untar
    if '.zip' in fixed_submission:
        print '** Submission uses zip file rather than tarfile.\n'
        cmd = 'unzip ./' + fixed_submission + ' > /dev/null'
    if '.tar' in fixed_submission:
        if 'tar.gz' in fixed_submission:
            cmd = 'tar xfvz ./' + fixed_submission + ' > /dev/null'
        elif 'tar.bz' in fixed_submission:
            cmd = 'tar xfv ./' + fixed_submission + ' > /dev/null'
        else:
            cmd = 'tar xfv ./' + fixed_submission + ' > /dev/null'
        #print '** Found tar file'
    elif '.tgz' in fixed_submission:
        cmd = 'tar xfv ./' + fixed_submission + ' > /dev/null'
        #print '** Found gzipped tar file'
    print '\n   --- Error messages from tar (if any) follow ---'
    os.system(cmd)
    print '   --- End of tar error messages ---'
    # rm the copied tar ball
    cmd = 'rm ' + fixed_submission
    os.system(cmd)
    return

def locate_exe(submission):
    #must have either makefile or 412fe script

    print "\nChecking for the executable '412fe'"

    fName = ''
    subDir = os.getcwd()

    if os.access('./Makefile',os.F_OK):
        fName = './Makefile'
    elif os.access(subDir+'./makefile',os.F_OK):
        fName = './makefile'

    if fName != '':
        if os.access(fName,os.R_OK | os.W_OK):
            print '   Found a Makefile'
            print '   --- Error messages from make (if any) follow ---'
            os.system('make clean >/dev/null')
            os.system('make build >/dev/null')
            os.system('make >/dev/null')  # backup plan in case no make 'build'
            print '   --- End of error messages from make ---\n'

            if os.access('./412fe',os.F_OK):
                if os.access('./412fe',os.X_OK):
                    print '412fe found with correct permissions'
                else:
                    print '412fe found but it lacks execute permission'
            else:
                print 'Did not find 412fe'

    else:
        print '   --- Makefile is not in the top-level directory'
        print '   --- Will look deeper, but you should fix this situation\n '
        os.system('find -iname "makefile" > tmp')
        f = open('tmp', 'r')
        line = f.readline()
        next = f.readline()
        while next != "":
            if len(next) < len(line):
                line = next
                next = f.readline()            
        f.close()

        os.system('rm tmp')
        if line != "":
            print '\n   --- Output from make (if any) follows ---'
            os.chdir(line.strip().rsplit('/', 1)[0])
            os.system('make clean')
            os.system('make build')
            os.system('make')
            print '   --- End of output from make ---\n'
        else: 
            print 'Archive does not contain a Makefile'
            print 'Will check for script'

        if os.access('./412fe',os.F_OK):
            if os.access('./412fe',os.X_OK):
                print '412fe found with correct permissiond'
            else:
                print '412fe found but it lacks execute permission.'
        else:
            print 'Did not find 412fe'

        return




