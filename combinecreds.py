#!/usr/bin/python

import sys, getopt, os, re

def main(argv):

    cacheloc = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('Format must be... combinecache.py -i <inputlocation> -o <outputfile>')
        sys.exit(2)
    for opt, args in opts:
        if opt == '-h':
           print('combinecache.py -i <inputlocation> -o <outputfile>')
           sys.exit()
        elif opt in ("-i", "--ifile"):
            cacheloc = args
            print('Cache location is ', cacheloc)
        elif opt in ("-o", "--ofile"):
            outputfile = args
            print('Output file is ', outputfile)

    print("Enumerating all the files in the location...")

    files = []
    folders = []
    cached = []
    secrets = []

    for (path, dirnames, filenames) in os.walk(cacheloc):
        folders.extend(os.path.join(path, name) for name in dirnames)
        files.extend(os.path.join(path, name) for name in filenames)

# Read in contents of a file

    print("Reading in contents of each file...")

# Loop through contents of cache/secrets logs

    for (file) in files:
        basefilename = os.path.basename(file)
        print("Reading " + basefilename)
        if file.endswith(".cached"):
            with open(file) as file_in:
                for line in file_in:
                    cached.append(basefilename + "::" + line)
        elif file.endswith(".secrets"):
            with open(file) as file_in:
                for line in file_in:
                    secrets.append(basefilename + "::" + line)

    print("Writing collected data out to two files...")

# Append each line to a new combined files with an extra field for the target source from file name

    f=open(outputfile+'_cached.txt','w')
    for line in cached:
        f.write(line)
    print("Cached Credentials written to "+outputfile+'_cached.txt')

    f=open(outputfile+'_secrets.txt','w')
    for line in secrets:
        f.write(line)            
    print("Secrets written to "+outputfile+'_secrets.txt')

    print("Finished")

if __name__ == "__main__":
    main(sys.argv[1:])
