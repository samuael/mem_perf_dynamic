import sys
import csv
import argparse
import string
from os import listdir 
from os.path import isfile  , join 
# import numpy as np
# from create_callgraph import *




releases = [  "memcached-1.4.22" , "memcached-1.4.30" , "memcached-1.5.12" , "memcached-1.5.39" , "memcached-1.6.9" ];
categories = [ "Load"  , "LoadStore" , "Nop" , "Store" , "Before" , "WithBranch"  ];
threads = [  4  , 8 , 16 ];
workloads = [ "workloada" , "workloadb" , "workloadc" , "workloadd" , "workloade"  , "workloadf"];



def readFile(summary, file_path):
  with open(file_path) as file:
    content = csv.reader(file , delimiter=' ' )
    for row in content:
      if len(row) < 2:
        continue
      data = [x for x in row if x != '']
      if not len(data) >2:
        continue; 
      if data[0] == 'queries:':
        if 'queries' in summary:
            summary['queries'] = summary['queries'] + int(data[1])
        else:
            summary['queries'] = int(data[1])

      if  len(data)>1  and data[1]== 'cycles':
        if 'cycles' in summary:
            summary['cycles'] = summary['cycles'] + int(data[0])
        else:
            summary['cycles'] = int(data[0])

      if data[1] == 'branch-misses':
        if 'branch-misses' in summary:
            summary['branch-misses'] = summary['branch-misses'] + int(data[0])
        else:
            summary['branch-misses'] = int(data[0])
        try:
          # print(float(data[3].strip("%")), type(float(data[3].strip("%"))))
          if [float(data[3].strip("%")) >0 ]:
            if 'branch-misses-(%)' in summary:
              summary['branch-misses-(%)'] = summary['branch-misses-(%)'] + float(data[3].strip("%"))
            else:
              summary['branch-misses-(%)'] = float(data[3].strip("%"))
        except Exception , e:
          print( str(e) );
          return None;

      if data[1] == 'branches':
        if 'branches' in summary:
            summary['branches'] = summary['branches'] + int(data[0])
        else:
            summary['branches'] = int(data[0])

      if data[1] == 'branch-loads':
        if 'branch-loads' in summary:
            summary['branch-loads'] = summary['branch-loads'] + int(data[0])
        else:
            summary['branch-loads'] = int(data[0])

      if data[1] == 'branch-load-misses':
        if 'branch-load-misses' in summary:
            summary['branch-load-misses'] = summary['branch-load-misses'] + int(data[0])
        else:
            summary['branch-load-misses'] = int(data[0])
            
      if data[1] == 'L1-icache-load-misses':
        if 'L1-icache-load-misses' in summary:
            summary['L1-icache-load-misses'] = summary['L1-icache-load-misses'] + int(data[0])
        else:
            summary['L1-icache-load-misses'] = int(data[0])

def writeSetToFile(s, file):
	original_stdout = sys.stdout # Save a reference to the original standard output
	with open(file, 'w') as f:
		sys.stdout = f # Change the standard output to the file we created.
		for i in s:
			print(str(i))
		sys.stdout = original_stdout # Reset the standard output to its original value

def writeDictToCSV(d, d1, dd, file):
	original_stdout = sys.stdout # Save a reference to the original standard output
	with open(file, 'w') as f:
		sys.stdout = f # Change the standard output to the file we created.
		for k,v in sorted(d.items()):
			print(str(k) + ',\t' + str(d1[k]) + ',\t' + str(v) + ',\t' + str(dd[k]))
		sys.stdout = original_stdout # Reset the standard output to its original value
summaryBase = dict()
# in this step i will loop over all the files and directories in the  output folder and collect their data in a specified file.
# first i will start with the name of the categories i labeled 
# the Order of the categories will be [  "Before"  , "LoadAfter" , "LoadAndStoreAfter" , "NopAfter" , "StoreAfter"      ]
# List of releases Used are [ "memcached-1.4.22"   , "memcached-1.4.30"   , "memcached-1.5.12"  , "memcached-1.5.20"  ,"memcached-1.6.9"     ]
# List of Threads [ "4" , "8" , "16"  ]
categories = [  "Before" , "LoadAfter" , "LoadAndStoreAfter" , "NopAfter" , "StoreAfter"      ];
releases = [ "memcached-1.4.22"   , "memcached-1.4.30"   , "memcached-1.5.12"  , "memcached-1.5.20"  ,"memcached-1.6.9"     ];
threads = [ "4" , "8" , "16"  ];

for category in categories:
  for thread in threads:
    cycles =[];
    branches =[];
    branch_misses =[];
    branch_misses_per=[];
    branch_loads=[];
    branch_load_misses=[];
    l1_icache_load_misses=[];
    for release in releases:
      # list all files in the directory and fetch all the data in them.
      filesDirectory = category+"/"+thread+"/" + release+"/";
      files = [  f for f in listdir(filesDirectory ) if isfile(join( filesDirectory , f)) ]
      # this dictionary file will hold the list of information such as 
      # cycles , branches , branch-loads  , branch-misses , branch-load-misses , branch-misses-percentage , L1-icache-misses
      total = dict()
      counter = 0;
      for sfile in files:
        readFile(total , filesDirectory+sfile)
        counter+=1;
        # taking the average of all categories 
      for a in total:
        total[a]=total[a]/counter;
        # writing in a file ... 
      with open( filesDirectory+"file.csv" , "w") as f:
        original_stdout = sys.stdout
        sys.stdout = f
        for a in total:
          print(  str(a)+",\t"+str(total[a]) )
      sys.stdout= original_stdout;
    # looping over each releases and getting the file.csv data insert it in the cycles , branched , 
    # branch-load , .. etc file accordingly.... 
    threadFileDirectory = category+"/"+thread+"/";
    for release in releases:
      # loop over all releases and append the cycles interger into cycles, branches to branches
      with open( threadFileDirectory+release+"/"+"file.csv"  , 'r') as fil:
        reader = csv.reader(fil);
        mdimensionalArr = list(reader);
        for a in mdimensionalArr:
          if len(a)==2:
            if (a[0]).strip()=="cycles":
              cycles.append(int((a[1]).strip()))
            elif (a[0]).strip()=="branches":
              branches.append(int((a[1]).strip()))
            elif (a[0]).strip()=="branch-loads":
              branch_loads.append(int((a[1]).strip()))
            elif (a[0]).strip()=="L1-icache-load-misses":
              l1_icache_load_misses.append(int((a[1]).strip()))
            elif (a[0]).strip()=="branch-load-misses":
              branch_load_misses.append(int((a[1]).strip()))
            elif (a[0]).strip()=="branch-misses":
              branch_misses.append(int((a[1]).strip()))
            elif (a[0]).strip()=="branch-misses-(%)":
              branch_misses_per.append(float((a[1]).strip()))
      # finished collecting data from file of a release.
    # Now I am gonna write the data into a file which is specifically created for 
    # cycles , branched , .. etc
    with open(threadFileDirectory+"cycles.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([cycles]);
    with open(threadFileDirectory+"branches.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([branches]);
    with open(threadFileDirectory+"branch-loads.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([branch_loads]);
    with open(threadFileDirectory+"L1-icache-load-misses.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([l1_icache_load_misses]);
    with open(threadFileDirectory+"branch-load-misses.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([branch_load_misses]);
    with open(threadFileDirectory+"branch-misses.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([branch_misses]);
    with open(threadFileDirectory+"branch-misses-per.csv" , "w") as f:
      writer = csv.writer(f);
      writer.writerows([branch_misses_per]);
    # Finished writing the files into 
  #for the categories i am gonna create each categories meaning 
  # cycles , branches , branch-misses , branch-loads , branch-load-misses , ... etc 
  fileDir = category+"/";
  cycles =[];
  branches =[];
  branch_misses =[];
  branch_misses_per=[];
  branch_loads=[];
  branch_load_misses=[];
  l1_icache_load_misses=[];
  for thread in threads:
    with open(fileDir+thread+"/"+"cycles.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      cycles.append(cykl[0])
    with open(fileDir+thread+"/"+"branches.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      branches.append(cykl[0])
    with open(fileDir+thread+"/"+"branch-loads.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      branch_loads.append(cykl[0])
    with open(fileDir+thread+"/"+"L1-icache-load-misses.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      l1_icache_load_misses.append(cykl[0])
    with open(fileDir+thread+"/"+"branch-load-misses.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      branch_load_misses.append(cykl[0])
    with open(fileDir+thread+"/"+"branch-misses.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      branch_misses.append(cykl[0])
    with open(fileDir+thread+"/"+"branch-misses-per.csv") as f:
      reader = csv.reader(f);
      cykl= list(reader)
      branch_misses_per.append(cykl[0])
  # create teh csv files and append the files there for each Category
  # Here , Category means Before , LoadAfter , LoadStoreAfter ... etc 
  with open(fileDir+"cycles.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(cycles);
  with open(fileDir+"branches.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(branches);
  with open(fileDir+"branch-loads.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(branch_loads);
  with open(fileDir+"L1-icache-load-misses.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(l1_icache_load_misses);
  with open(fileDir+"branch-load-misses.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(branch_load_misses);
  with open(fileDir+"branch-misses.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(branch_misses);
  with open(fileDir+"branch-misses-per.csv" , "w") as f:
    writer = csv.writer(f);
    writer.writerows(branch_misses_per);
