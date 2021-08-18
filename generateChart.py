
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import csv


categories = [  "Before" , "LoadAfter" , "LoadAndStoreAfter" , "NopAfter" , "StoreAfter"      ];
releases = [ "memcached-1.4.22"   , "memcached-1.4.30"   , "memcached-1.5.12"  , "memcached-1.5.20"  ,"memcached-1.6.9"     ];
threads = [ "4" , "8" , "16"  ];
# workloads = [ "workloada" , "workloadb" , "workloadc" , "workloadd" , "workloade"  , "workloadf"];
scategories = ["cycles"    ,"branches",    "branch-misses"   , "branch-misses-(%)",   "branch-loads",      "branch-load-misses",'L1-icache-load-misses']
fcategories = ["cycles.csv","branches.csv","branch-misses.csv","branch-misses-per.csv","branch-loads.csv", "branch-load-misses.csv" ,"L1-icache-load-misses.csv" ]

for category in categories:
    categoryDir = category+"/";
    for thread in threads :
        index =0;
        threadDir = categoryDir+thread+"/";
        for scat in scategories:
            index+=1;
            with open( threadDir+ fcategories[index-1] , "r" ) as fi:
                reader = csv.reader(fi , delimiter=",");
                datas = list(reader);
                # Now I have the array what i have to do is Generate the Plot in this file 
                # adding the datas in this loop for example The Thread  , Category  , scat( representing the Name of The section category )
                # Like cycles , branches , branch-misses  , branche-loads , branch-load-misses.
                if len(datas)==1:
                    plt.plot(releases , datas[0]  , label="After")
                    # plt.plot(dev_x , dev_another , label="Another")
                    plt.style.use('fivethirtyeight')
                    plt.legend()
                    plt.xlabel("Releases")
                    plt.ylabel("scat")
                    plt.title( category +" Thread : "+ str(thread)+' '+scat )
                    plt.savefig( threadDir+scat+".pdf")
                    # plt.show()
        # finished building a graph for a categories of a thread.
        
