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




#parser = argparse.ArgumentParser(description='Post process two mysql versions')
#parser.add_argument('--version', help='old input file path')
#parser.add_argument('--base', help='new input file path')
#parser.add_argument('--load', help='new input file path')
# parser.add_argument('--store', help='new input file path')
# parser.add_argument('--nop', help='new input file path')
# parser.add_argument('--thread', help='the benchmark has how many threads')
# parser.add_argument('--bench-name', help='the benchmark has how many threads')

# args = parser.parse_args()
# version = str(args.version)
# base = str(args.base)
# load = str(args.load)
# store = str(args.store)
# nop = str(args.nop)
# thread = str(args.thread)
# bench_name = str(args.bench_name)

# input_path ='/proj/benchframe-PG0/mysql_perf_for_emitted_binaries/'

summaryBase = dict()
#for e in np.arange(1,11,1):
# readFile(summaryBase, 'memcached-1.4.22_workloada_4_after_run.txt')
# readFile(summaryBase  , "newOne.txt" )

# summary = dict()
# for e in np.arange(1,11,1):
#    readFile(summary, '_name+'_240sec_exec_'+ str(e)+'.txt')
#
# diff = dict()
# for k in summary.keys():
#     diff[k] = float(summary[k] /summaryBase[k])
#     summary[k] = float(summary[k] / 10)
#     summaryBase[k] = float(summaryBase[k] / 10)


# writeDictToCSV(summary, summaryBase, diff,'summary_stat_thread_.txt')
#for a in summaryBase:
#  print(a , summaryBase[a]);





# in this step i will loop over all the files and directories in the  output folder and collect their data in a specified file.
# first i will start with the name of the categories i labeled 
# the Order of the categories will be [  "Before"  , "LoadAfter" , "LoadAndStoreAfter" , "NopAfter" , "StoreAfter"      ]
# List of releases Used are [ "memcached-1.4.22"   , "memcached-1.4.30"   , "memcached-1.5.12"  , "memcached-1.5.20"  ,"memcached-1.6.9"     ]
# List of Threads [ "4" , "8" , "16"  ]
categories = [  "Before"  ] #, "LoadAfter" , "LoadAndStoreAfter" , "NopAfter" , "StoreAfter"      ];
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
      

            
