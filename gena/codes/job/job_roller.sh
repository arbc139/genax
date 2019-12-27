while true; do
	sleep $sleep_time;
	monthly="-02 07:00:00"
	daily="03:00:00"
	curr_date=$(date +"%Y-%m-%d %H:%M:%S")
	sleep_time="5.0"
	(echo "")&
	(echo "[$curr_date] New Job Check";python new_job.py --mysqlId=$1)&
	(echo "[$curr_date] Insert Check"; python insertor.py --mysqlId=$1)&
	(echo "[$curr_date] Weka Check"; python weka_start.py --mysqlId=$1)&
	(echo "[$curr_date] Net Check"; python net_start.py --mysqlId=$1)&
	if [[ "$curr_data" =~ "$daily" ]]; then
		(echo "[$curr_date] Daily Update"; python daily_update.py --mysqlId=$1)&
	fi
	if [[ "$curr_date" =~ "$monthly" ]]; then
		(echo "[$curr_date] Monthly Update"; python monthly_update.py --mysqlId=$1)&
	fi
done
