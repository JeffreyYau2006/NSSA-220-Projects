
#!/bin/bash
set -u

APP_DIR="./APMS"
APPS=("APM1" "APM2" "APM3" "APM4" "APM5" "APM6")
NIC="ens192"
IP_ADDR="192.168.197.1"
SYSTEM_FILE="system_metrics.csv"
PROC_SAMPLE_SEC=5
RUN_TIME=$((15 * 60))
START_TIME=$(date +%s)
APP_PIDS=()
COLLECTOR_PIDS=()

cleanup() {
	echo "Cleaning up..."
	if ((${#COLLECTOR_PIDS[@]})); then
		for cpid in "${COLLECTOR_PIDS[@]}"; do
			kill "$cpid" 2>/dev/null || true
		done
	fi

 	if ((${#APP_PIDS[@]})); then
		for pid in "${APP_PIDS[@]}"; do
			if kill -0 "$pid" 2>/dev/null; then
				echo "Killing app PID $pid"
				kill "$pid" 2>/dev/null || true
			fi
		done
	fi


	pkill -P $$ 2>/dev/null || true
	echo "All processes terminated."
}
trap cleanup EXIT

resolve_app_pid() {
	local app_path="$1"
	local app_name
	app_name=$(basename "$app_path")
	sleep 0.3
	pgrep -n "$app_name" || echo 0

}

spawn_apps() {
	echo "Launching applications..."
	APP_PIDS=()
	for app in "${APPS[@]}"; do
		local app_path="$APP_DIR/$app"
		if [[ -x "$app_path" ]]; then
			echo "Starting $app $IP_ADDR"
			"$app_path" "$IP_ADDR" >/dev/null 2>&1 &
			local real_pid
			real_pid=$(resolve_app_pid "$app_path")
			APP_PIDS+=("$real_pid")
			echo "$app running as PID $real_pid"
		else
			echo "ERROR: $app_path not found or not executable" >&2
		fi
	done
}

collect_system_metrics() {
	echo "seconds,RX_kBps,TX_kBps,DiskWrites_kBps,AvailDisk_MB" > "$SYSTEM_FILE"

	while true; do
		local loop_start now elapsed
		loop_start=$(date +%s)
		local rx="" tx=""
		read rx tx < <(LC_ALL=C /usr/bin/ifstat -n -i "$NIC" 1 1 2>/dev/null | awk 'NR==3 {print $1, $2}')
		rx=${rx:-0}; tx=${tx:-0}
		local disk_writes
		disk_writes=$(LC_ALL=C iostat -d sda 1 2 2>/dev/null | awk '
			BEGIN{v=0}
			$1=="sda"{last=$0}
			END{
				split(last,a)
				c=0
				for(i=1;i<=length(a);i++){ if (a[i] ~ /^-?[0-9.]+$/){ c++; if(c==3){print a[i]; exit}}}
				print 0
			}')
		local avail_disk
		avail_disk=$(df -m / 2>/dev/null | awk 'NR==2 {print $4+0}')

		now=$(date +%s)
		elapsed=$(( now - START_TIME ))
		echo "$elapsed,$rx,$tx,$disk_writes,$avail_disk" >> "$SYSTEM_FILE"

    		local spent=$(( $(date +%s) - loop_start ))
    		local remain=$(( PROC_SAMPLE_SEC - spent ))
    		(( remain > 0 )) && sleep "$remain"
	done
}

collect_process_metrics() {
	local index=0
	for pid in "${APP_PIDS[@]}"; do
		local app="${APPS[$index]}"
		local outfile="${app}_metrics.csv"
		echo "seconds,%CPU,%MEM" > "$outfile"

		(
			sleep 1
			while true; do
				local now elapsed
				now=$(date +%s)
				elapsed=$(( now - START_TIME ))

				if ! kill -0 "$pid" 2>/dev/null; then
					echo "$elapsed,0,0" >> "$outfile"
					break
				fi

				read cpu mem < <(ps -p --no-headers -p "$pid" -o %cpu,%mem 2>/dev/null)
				cpu=${cpu:-0}; mem=${mem:-0}
				printf "%d,%.2f,%.2f\n" "$elapsed" "$cpu" "$mem" >> "$outfile"

				sleep "$PROC_SAMPLE_SEC"
			done
		) &
		COLLECTOR_PIDS+=("$!")
		((index++))
	done
}

echo "Starting APM tool..."
spawn_apps
collect_system_metrics &
COLLECTOR_PIDS+=("$!")
collect_process_metrics
sleep "$RUN_TIME"

