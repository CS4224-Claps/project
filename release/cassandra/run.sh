#! /usr/bin/env bash
hosts=()
db="cassandra"

if [ ! -f config.json ]; then
    echo "Please put a config.json in the current folder"
    exit 1
else
    echo "Found config.json... Please check if it is correct!"
    cat config.json
    echo ""
fi

echo "Where is the project root located?"
read project_root

if [[ $(whoami) == "cs4224d" ]]; then
    hosts=("xcnd35" "xcnd36" "xcnd37" "xcnd38" "xcnd39")

    echo "Which workload are you running? (A or B)"
    read workload # A or B
    workloadpath="~/seed/xact_files_$workload"
    unset workload
else
    while [ ${#hosts[@]} -ne 5 ]; do
        echo "Please input 5 hostname separated by whitespace";
        read -a hosts
    done

    echo "Enter path to the workload you are running"
    read workloadpath
fi 

i=0
for host in ${hosts[@]}; do
    echo "--------------------
    $host
--------------------"
    sshcmd="
cd $project_root;
mkdir -p logs/$db;
nohup python3 -u run_clients.py --db $db -n $i -i $workloadpath >logs/$db/$host.log 2>&1 & "
    echo $sshcmd
    ssh -o LogLevel=Error $host "$sshcmd"
    ((i++))
done
