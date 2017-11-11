while true; do
	sleep $sleep_time;
	re="-02 07:00:00"
	curr_date=$(date +"%Y-%m-%d %H:%M:%S")
	sleep_time="5.0"
	(echo "")&
	(echo "[$curr_date] New Job Check";python new_job.py --mysqlId=$1)&
	(echo "[$curr_date] Insert Check"; python insertor.py --mysqlId=$1)&
	(echo "[$curr_date] Weka Check"; python weka_start.py --mysqlId=$1)&
	(echo "[$curr_date] Net Check"; python net_start.py --mysqlId=$1)&
	if [[ "$curr_date" =~ "$re" ]]; then
		(echo "[$curr_date] Monthly Update"; python monthly_update.py --mysqlId=$1)&
	fi
done
