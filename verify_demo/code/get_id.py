#!/usr/bin/python

import os

def get_id():
    file_name = ''

    print '\nChecking README file\n'

    if os.path.isfile('./README'):
        file_name = './README'
    elif os.path.isfile('./readme'):
        file_name = './readme'
        print '** README file should be named in uppercase letters.\n'

    if file_name == '':
        README = 0
        NAME = 'no name found'
        NETID = ' no netid found'
        return
    else:
        README = 1

    cmd = 'grep NAME '+file_name+' >./temp'
    #print cmd
    os.system(cmd)
    f = open("./temp", 'r')
    line = f.readline()
    if 'NAME' in line:
        NAME = line.rsplit(':', 1)[1].strip()
    f.close()
    os.system('rm ./temp')

    cmd = 'grep NETID '+file_name+' >./temp'
    #print cmd
    os.system(cmd)
    f = open("./temp", 'r')
    line = f.readline()
    if 'NETID' in line:
        NETID = line.rsplit(':', 1)[1].strip()
    f.close()
    os.system('rm ./temp')

    # expected case                                                           
    if README == 1 and NAME != '' and NETID != '':
        print "README specifies name '"+NAME+"' and netid '"+NETID+"'"

    else:
        if README == 0:
            print 'No README found'

        if NAME != '':
            print 'Found name: ',NAME
        else:
            print 'Name not found'

        if NETID != '':
            print 'Found netid: ',NETID
        else:
            print 'Netid not found'

    return 


