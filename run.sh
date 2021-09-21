#! /usr/bin/env bash
hosts=()

echo "Where is the project root located?"
read project_root

echo "Which db are you using? (cassandra or cockroachdb)"
read db

if [[ $(whoami) != "cs4224d" ]]; then
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
nohup python3 -u run_clients.py --db $db -n $i -i $workloadpath >logs/cockroachdb/$host.log 2>&1 & "
    echo $sshcmd
    ssh -o LogLevel=Error $host "$sshcmd"
    ((i++))
done
