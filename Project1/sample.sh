#!/bin/bash
set -u

APP_DIR="./APMS"
APPS=("APM1" "APM2" "APM3" "APM4" "APM5" "APM6")


NIC="ens33"
IP_ADDR="192.168.197.1"

SYSTEM_FILE="system_metrics.csv"
PROC_SAMPLE_SEC=5
RUN_TIME=$((15 * 60))
START_TIME=$(date +%s)

APP_PIDS=()
COLLECTOR_PIDS=()

cleanup() {

    # kill per-process collectors
    if ((${#COLLECTOR_PIDS[@]})); then
        for cpid in "${COLLECTOR_PIDS[@]}"; do
            kill "$cpid" 2>/dev/null || true
        done
    fi

    # kill app processes
    if ((${#APP_PIDS[@]})); then
        for pid in "${APP_PIDS[@]}"; do
            if [ "$pid" -gt 1 ] && kill -0 "$pid" 2>/dev/null; then
                echo "Killing $pid"
                kill "$pid" 2>/dev/null || true
            fi
        done
    fi

    # last resort – kill children of this script
    pkill -P $$ 2>/dev/null || true

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
    echo "Launching applications:"
    APP_PIDS=()
    for app in "${APPS[@]}"; do
        local app_path="$APP_DIR/$app"
        if [[ -x "$app_path" ]]; then
            echo "Starting $app $IP_ADDR"
            "$app_path" "$IP_ADDR" >/dev/null 2>&1 &
            local real_pid
            real_pid=$(resolve_app_pid "$app_path")
            if [ "$real_pid" -gt 1 ]; then
                APP_PIDS+=("$real_pid")
                echo "$app running as PID $real_pid"
            else
                echo "could not resolve PID for $app" >&2
            fi
        else
            echo "ERROR: $app_path not found or not executable" >&2
        fi
    done
}

collect_system_metrics() {
    # NO HEADER – rubric wants numbers only
    : > "$SYSTEM_FILE"

    while true; do
        local loop_start now elapsed
        loop_start=$(date +%s)

        # network (rx, tx) in kB/s
        read rx tx < <(LC_ALL=C ifstat -n -i "$NIC" 1 1 2>/dev/null | awk 'NR==3 {print $1, $2}')
        rx=${rx:-0}; tx=${tx:-0}

        # disk writes in kB/s for sda
        # -dk to get kB directly; 1 1 = one report
        local disk_writes
        disk_writes=$(LC_ALL=C iostat -dk 1 1 2>/dev/null | awk '$1=="sda"{print $4; exit}')
        disk_writes=${disk_writes:-0}

        # available disk on /
        local avail_disk
        avail_disk=$(df -m / 2>/dev/null | awk 'NR==2 {print $4+0}')

        now=$(date +%s)
        elapsed=$(( now - START_TIME ))
        echo "$elapsed,$rx,$tx,$disk_writes,$avail_disk" >> "$SYSTEM_FILE"

        # keep at ~5 seconds
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

        # NO HEADER – rubric wants plain rows
        : > "$outfile"

        (
            sleep 1
            while true; do
                local now elapsed
                now=$(date +%s)
                elapsed=$(( now - START_TIME ))

                if ! kill -0 "$pid" 2>/dev/null; then
                    # app died – log zero once and quit
                    echo "$elapsed,0,0" >> "$outfile"
                    break
                fi

                # correct ps form
                read cpu mem < <(ps --no-headers -p "$pid" -o %cpu,%mem 2>/dev/null)
                cpu=${cpu:-0}; mem=${mem:-0}
                printf "%d,%.2f,%.2f\n" "$elapsed" "$cpu" "$mem" >> "$outfile"

                sleep "$PROC_SAMPLE_SEC"
            done
        ) &
        COLLECTOR_PIDS+=("$!")
        ((index++))
    done
}

spawn_apps
collect_system_metrics &
COLLECTOR_PIDS+=("$!")
collect_process_metrics

# run for 15 minutes
sleep "$RUN_TIME"
