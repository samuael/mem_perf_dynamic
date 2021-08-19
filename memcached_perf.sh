#!/bin/bash
#
#
#
#  PARAMETERS : $1 = YCSB WORKLOADS DIRECTIORY
#               $2 = MEMCACHED RELEASES DIRECTORY

clear;
if $# -lt 3
then
        clear;
        echo "Unexpected Operands Length : Please user  ycsb /path/to/ycsb/workloads/ /path/to/memcached/realeases/directory";
        return;
fi

current_directory=$(pwd);

for releaseo in memcached-1.4.22  memcached-1.4.30  memcached-1.4.39  memcached-1.5.12  memcached-1.5.20  memcached-1.6.9
do
        cp $2/$releaseo/memcached $2/$releaseo/memcachedBefore;   #to be cahnged to memcached and perform the install and perf on 
        cp $2/$releaseo/memcached $2/$releaseo/memcachedOriginal; # To recover the binary again ... 
done

mkdir -p output 
for category in Before LoadAfter LoadAndStoreAfter  NopAfter StoreAfter 
do
        mkdir -p output/$category;
        for thread in 4 8 16
        do 
                CPUSET=2-$((  thread +1  ));
                mkdir -p output/$category/$thread;
                for release in memcached-1.4.22  memcached-1.4.30  memcached-1.5.12  memcached-1.5.20  memcached-1.6.9
                do 
                        mkdir -p output/$category/$thread/$release;
                        for emit in 2 4 8;
                        do

                                cd $2/$release;
                                if [ "$category" = "Begin"   ];
                                then
                                        # This is gonna be execute only for the Begin Category and this will be 
                                        mv memcached$release memcached;
                                else
                                        mv memcached${release}_${emit} memcached;
                                fi
                                sudo make install;
                                memcached  -d -m 1024 -u root -l 127.0.0.1 -p 11211 -t 4;
                                if [[ ! $(pidof memcached) ]]
                                then
                                        echo "Memcached( -- memcached${release}_${emit} -- ) is not running ...";
                                        return;
                                fi
                                cd $current_directory;
                                echo "  CPU SET in workloads $CPUSET ";
                                # make the new directory and isntall it using make install 
                                for workload in  workloada workloadb workloadc workloadd workloade workloadf;
                                do 
                                        sudo perf stat -a  -C ${CPUSET}  -e cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses --no-big-num -- sudo ./bin/ycsb load memcached --threads ${thread} -s -P $1/$workload  -p "memcached.hosts=127.0.0.1:11211" &> /dev/null;
                                        if [ $release  = "Begin" ]
                                        then 

                                                sudo perf stat -a -C ${CPUSET} -e cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses  --no-big-num  -- sudo ./bin/ycsb run memcached  --threads ${thread} -s -P  $1/$workload  -p "memcached.hosts=127.0.0.1:11211" &> output/$category/$thread/$release/${release}_${workload}_Run.txt;
                                        else 
                                                sudo perf stat -a -C ${CPUSET} -e  cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses --no-big-num -- sudo ./bin/ycsb run memcached  --threads ${thread} -s -P  $1/$workload  -p "memcached.hosts=127.0.0.1:11211" &> output/$category/$thread/$release/${release}_${emit}_${workload}_Run.txt;
                                        fi 
                                done 
                        done 
                done 
        done 

done






# for  release in  memcached-1.4.22  memcached-1.4.30  memcached-1.4.39  memcached-1.5.12  memcached-1.5.20  memcached-1.6.9
# do
#         # Where $2 is the path to the memcached releases.
#         cd $2/$release; 
# 	# change the name to memcached_main and continue to process
# 	cp  memcached memcached_original;
# 	mv memcached  memcached_main;
#         for binary in memcached_main memcachedLoadAfter_2 memcachedLoadAfter_4 memcachedLoadAfter_8
#         do
#                 mv $binary memcached;
#                 sudo make install;
#                 memcached  -d -m 1024 -u root -l 127.0.0.1 -p 11211 -t 4;
#                 if [[ ! $(pidof memcached) ]]
#                 then
#                         echo "Memcached(${binary}) is not running ...";
#                         return;
#                 fi
#                 mkdir -p $2/$release/$binary;
#                 # Now the memecached is installed
#                 # mkdir -p  output/$release/;
#                 for  workload in workloada workloadb workloadc workloadd workloade workloadf
#                 do
#                         for THREADS in 4 8 16
#                         do
#                                 CPUSET=2-$((  THREADS+1  ))
#                                 mkdir -p output/$release/$THREADS;
#                                 touch output/$release/$THREADS/${release}_${workload}_Load.txt;
#                                 touch output/$release/$THREADS/${release}_${workload}_Run.txt;
#                                 sudo perf stat -e -C ${CPUSET}  cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses -- sudo ./bin/ycsb load memcached --threads=${THREADS} -s -P $1/$workload  -p "memcached.hosts=127.0.0.1:11211" &> output/$release/$THREADS/${release}_${workload}_Load.txt;
#                                 sudo perf stat -e -C ${CPUSET}  cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses -- sudo ./bin/ycsb run memcached  --threads=${THREADS} -s -P  $1/$workload -p "memcached.hosts=127.0.0.1:11211" &> output/$release/$THREADS/${release}_${workload}_Run.txt;
#                         done
#                 done
#         done 
#         cd $current_directory;


#         echo "$2/$release";
#         cd $2/$release;
#         sudo mv memcached memcached_before
#         sudo mv memcached_after memcached;
#         sudo make install;
#         memcached  -d -m 1024 -u root -l 127.0.0.1 -p 11211 -t 4;
#         memcached  --version;

# 	if [[ !$(pidof memcached) ]]
#         then
#       		echo "Memcached After is also not running ";
# 		return;
#         fi
#         cd $current_directory;
#         #OUTPUT_DIR = "${release}_output";
#         mkdir -p output/$release/${release}_after_pass;
#         for  workload in workloada workloadb workloadc workloadd workloade workloadf
#         do
#                 for THREADS in 4 8 16
#                 do
# 			mkdir -p output/$release/${release}_after_pass/$THREADS;
#                         CPUSET=2-$(( THREADS+1 ))
#                         touch output/$release/${release}_after_pass/$THREADS/${release}_${workload}_Load.txt;
#                         touch output/$release/${release}_after_pass/$THREADS/${release}_${workload}_Run.txt;
#                         sudo perf stat -e -C ${CPUSET} cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses -- sudo ./bin/ycsb load memcached --threads=${THREADS} -s -P $1/$workload  -p "memcached.hosts=127.0.0.1:11211" &>  output/$release/${release}_after_pass/$THREADS/${release}_${workload}_Load.txt;
#                         sudo perf stat -e -C ${CPUSET} cycles,branches,branch-misses,branch-loads,branch-load-misses,L1-icache-load-misses -- sudo ./bin/ycsb run memcached  --threads=${THREADS} -s -P $1/$workload -p "memcached.hosts=127.0.0.1:11211" &> output/$release/${release}_after_pass/$THREADS/${release}_${workload}_Run.txt;
#                 done
#         done
#         cd $2/$release;
#         sudo mv memcached memcached_after;
#         sudo mv memcached_before memcached;
#         cd $current_directory;
# done
