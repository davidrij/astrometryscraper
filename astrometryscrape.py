#Script to scrape nova.astrometry.net and generate star database with attitudes and link to image

import os
import time
import csv
import ast

waittime = 0.05 #seconds, time for the program to wait for entry search
csv_columns = ["jobnumber","status", "machine_tags", "parity", "orientation", "pixscale", "radius", "ra", "dec", "tags", "original_filename", "objects_in_field"]

writerfile = open('database.csv','a', newline='')
outfile = open('database.csv')
reader = csv.DictReader(outfile)
lastjob = 0

for lastjob in reader:
    pass
if lastjob is 0:
    #write database headers
    print("Empty database, adding header")
    writer = csv.DictWriter(writerfile, fieldnames=csv_columns)
    writer.writeheader()
    jobstart = 0
else:
    jobstart = int(lastjob["jobnumber"])+1
    print("Starting at job number:",jobstart) 
    
outfile.close()
writerfile.close()

#try for 10 million entry numbers
for i in range(jobstart,10000000):
    print("Trying for:", i)
    time.sleep(waittime) #wait for waittime seconds in order to give the website some rest!
    page = "http://nova.astrometry.net/api/jobs/" + str(i) + "/info"
    os.system('wget -O temp.txt ' + str(page))
    with open('temp.txt', 'r') as infile, open('database.csv','a') as outfile:
        line = infile.read()
        if "success" in line:
            
            #clean string
            line = line.replace('"calibration": {', '')
            line = line.replace('},', ',')

            #convert string line to dictionary
            data = ast.literal_eval(line) 
            data["jobnumber"] = i #append job number

            #write to csv
            writer = csv.DictWriter(outfile, fieldnames=csv_columns)
            writer.writerow(data)

        infile.close()
        outfile.close()


