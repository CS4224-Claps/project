hosts=( $1 $2 $3 $4 $5 )

if [ "${#hosts[@]}" == 5 ]
then
    for host in ${hosts[@]}
    do 
        sshcmd="cockroach start \
        --store=/temp/cs4224d/cockroachdb/data \
        --listen-addr=$host:26257 \
        --http-addr=$host:8080 \
        --join=$2:26257,$3:26257,$4:26257,$5:26257,$6:26257 \
        --insecure \
        --background"

        ssh -o LogLevel=Error $host "$sshcmd"
    done 
else 
    echo "You should only have 5 hosts. Please try again."
fi 
