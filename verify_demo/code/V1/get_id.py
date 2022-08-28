#!/usr/bin/python

import os

def check_file_type(type):
    for cdir, dirs, files in os.walk('./'):
        for file in files:
            if type in file:
                #if file.rsplit('.',1)[1].strip() == "i":
                #    return True
                return True
    return False


def get_id():
    found_README = 0;     
    file_name = ''
    name = ''
    netid = ''

    print 'Checking README file'

    if os.path.isfile('./README'):
        file_name = './README'
    elif os.path.isfile('./readme'):
        file_name = './readme'
        print '** README file should be named in uppercase letters.\n'

    if file_name == '':
        print '** no README file found. It should be in the top directory'
        return 'no name', 'no netid'

    cmd = 'grep NAME '+file_name+' >./temp'
    #print cmd
    os.system(cmd)
    f = open("./temp", 'r')
    line = f.readline()
    if 'NAME' in line:
        name = line.rsplit(':', 1)[1].strip()
    f.close()
    os.system('rm ./temp')

    cmd = 'grep NETID '+file_name+' >./temp'
    #print cmd
    os.system(cmd)
    f = open("./temp", 'r')
    line = f.readline()
    if 'NETID' in line:
        netid = line.rsplit(':', 1)[1].strip()
    f.close()
    os.system('rm ./temp')

    if name == '' or netid == '':
        print 'Missing NAME or NETID line(s) in README file'
        print ' '
    else:
        print 'Found NAME ('+name+') and NETID ('+netid+') in README file.'
    return name, netid


