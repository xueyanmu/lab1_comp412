#!/usr/bin/python

import os, time, calendar, datetime, sys

from datetime import datetime

from changeto_testlocation import change_to_test_location, locate_exe
from lab_grade import lab_grade_file, lab_missing_file_check, lab_help_message_check
from get_id import get_id
import operator

#
# Configuration parameters
#


# base_name contains the path to the directory where this file tree is installed
# It should be one level above the directory that holds this code.

#base_name = "/clear/courses/comp412/students/lab1/autograder/"
#base_name = "/clear/courses/comp412/Keith/Lab1/autograder/"
base_name = "/storage-home/x/xm14/comp412/autograderSetup/"
# Locations for test blocks (blocks) and timing blocks (timing)
# These are relative to the directory in base_name

blocks_dir = "auto_grade/blocks/"
timing_dir = "auto_grade/timing_blocks/"

# Points allotted, out of 100, for Conformance to Specifications,
# Correctness, and Efficiency
#
# These should sum to 100 
#

Conforms_Points = 35
Correct_Points  = 50
Scalability_Points = 15

def check_file_type(type):
    for cdir, dirs, files in os.walk('./'):
        for file in files:
            if type in file:
                return True
    return False

def run_timing_block(block_name):

    path = base_name + timing_dir

    command_line = "timeout 60.0s ./412fe "+path+block_name+" >&/dev/null"
    #print "command line: ", command_line
    
    start_tic = datetime.now()
    os.system(command_line)
    stop_tic  = datetime.now()
    elapsed = stop_tic - start_tic
    ms = (elapsed.days * 86400 + elapsed.seconds) * 1000 + elapsed.microseconds / 1000.0
    return ms
        
def run_test(submission):

    # have already found and built the executable
    #record name and netid in result file
    result_file.write(current_name + '\t' + current_id + '\t')

    print "Testing Correctness\n"

    sum_extras   = 0
    sum_misses   = 0
    sum_expected = 0
    
    path = base_name + blocks_dir
    for test in sorted(os.listdir(path)):
        if not '.i' in test:
            continue
        extras,found,missed,total = lab_grade_file(path,test)
        sum_expected += total
        print "\t"+test,
        print "\t"+str(extras)+" correct lines identified as errors"
        sum_extras += extras
        print "\t\t\t"+str(found)+" errors found, "+str(total)+" expected"
        sum_misses += missed

    print "\t-------------------------"
    print "\t"+str(sum_extras)+" correct lines identified as errors"
    print "\t"+str(sum_misses)+" lines with errors missed\n"

    correct = 100 - 100 * (sum_extras + sum_misses) / sum_expected
    
    # conformance testing
    # they get 50% if the tar file unpacks and runs ... that is,
    # they got this far in the autograder

    print "Testing Conformance\t(If we got this far, the tar file worked.)\n"
    conforms = 50
    
    # test for graceful handling of a bad file name
    missing_file = lab_missing_file_check(result_file)
    if missing_file == 0:
        print "\tNo 'ERROR' message on missing or bad file name"
    elif missing_file > 0:
        print "\tProduced 'ERROR' message on missing or bad file name"
        conforms += 25 * missing_file
    else:
        print "\tUnexpected corner case"

    # test for a helpmessage on the '-h' command-line option
    help = lab_help_message_check(result_file)
    if help == 0:
        print "\tNo help message found for '-h option"
    elif help < 4:
        print "\tHelp message is missing some mandated options  ("+str(help)+")"
    elif help == 4:
        print "\tHelp message check found all options"
    else:
        print "\tHelp message check found duplicate explanations"

    conforms += (help * 6.25)

    # Scalability testing
    scales = 0
    print "\nTesting Scalability:\n"

    t_names =  ["T8k.i","T16k.i","T32k.i","T64k.i","T128k.i"]
    t_sizes =  [8, 16, 32, 64, 128]
    t_times =  []
    for n in t_names:
        ms = run_timing_block(n)
        t_times.append(ms)

    for i in range(0,5):
        print "\t"+t_names[i]+":  \t"+str(t_times[i]/1000)+" seconds"

    fail_ct   = 0
    linear_ct = 0
    nonlin_ct = 0
    quad_ct   = 0
    for i in range(1,4):
        ratio = t_times[i+1]/t_times[i]
        if ratio < 1.1:
            fail_ct +=1
        if ratio < 2.3:
            linear_ct += 1
        elif ratio > 3.6:
            quad_ct += 1
        else:
           nonlin_ct += 1

    if fail_ct > 0:
        print "\n\tThe code may not work; "+str(fail_ct)+" codes showed no growth"
        scales = 0
    if nonlin_ct == 0:
        print "\n\tScaling appears to be linear"
        scales = 100
    elif nonlin_ct == 1:
        print "\n\tScaling may be linear with one heap-related jump"
        scales = 90
    elif quad_ct > 2:
        print "\n\tScaling appears to quadratic"
        scales = 0
    else:
        print "\n\tScaling appears to be non-linear"
        scales = 50

    # Report results
    print "\nScoring:"
    print "\tConformance:\t"+str(conforms)+"%"
    print "\tCorrectness:\t"+str(correct)+"%"
    print "\tScalability:\t"+str(scales)+"%"

    total = conforms * Conforms_Points  # broken up for readability
    total += correct * Correct_Points
    total += scales * Scalability_Points
    total = total/100

    print "\tTotal Points:\t"+str(total)

    result_file.write(str(conforms)+"\t"+str(correct))
    result_file.write("\t"+str(scales)+"\t"+str(total)+"\n")
    
    return 0


def main():
    global root
    global tests
    global blocks_dir
    global base_name
    global current_name
    global current_id
    global result_file
    global failed_file

    root = os.getcwd()

    #for each submission:
    #1. make a tmp dir
    #2. cp the tar ball to the dir
    #3. extract and the tar ball
    #4. locate the makefile or the executable
    #5. ready to run with the executable

    print 'Auto-grader Configuration:'
    print '  blocks found in :\t',blocks_dir

    # set up the output files
    result_path = base_name + 'result/'

    result_file = open(result_path + 'results.txt','w')
    failed_file = open(result_path + 'failed.txt','w')

    # write file headers
    result_file.write('Name\tNetId\tConform\tCorrect\tScales\tPoints\n')
    failed_file.write('Name\tNetId\n')

    print '======================================================================='
    
    for submission in os.listdir('./'):
        if os.path.isdir(submission):
            continue

        print 'Testing submission: ' + submission 
        submission_date = change_to_test_location(submission)
                
        current_name, current_id = get_id()
        if current_id == "":
            current_id   = submission.split('.', 1)[0]
            current_name = current_id

        print 'Name: ' + current_name + ', NetId: ' + current_id,
        print '\tDate From Files: ' + str(submission_date) + '\n'

        if not locate_exe(submission) == -1:
            dummy = run_test(submission)
        else:
            print 'submission failed to build correctly'
            print 'likely a problem with tar file, make file, or script'
            failed_file.write(current_name + '\t' + current_id+"\n")

        print '\nfinished testing submission ' + submission 
        print '======================================================================='

        #clean up everything that was created during testing
        os.chdir(root)
        fixed_submission = submission.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("'", "\\'")
        folder = submission.split('.', 1)[0]
        fixed_folder = fixed_submission.split('.', 1)[0]
        os.system('rm -rf ' + fixed_folder)


    # close the grading files
    result_file.close()
    failed_file.close()

    print ' '
    print 'Grading run complete.'
    exit(0)
    
if __name__ == "__main__":
    main()
