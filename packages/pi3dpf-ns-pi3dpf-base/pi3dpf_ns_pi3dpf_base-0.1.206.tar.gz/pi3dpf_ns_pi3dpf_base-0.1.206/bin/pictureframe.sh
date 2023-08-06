#!/bin/bash
THIS_FILE="$(basename "$0")"
THIS_DIR="$(dirname "$0")"
THIS_DIR_ABS="$(cd $THIS_DIR; pwd)"
export PF_ROOT="$(cd "$THIS_DIR_ABS"/..; pwd)"
PYTHON_PROJECT_LIBS="$(cd "$THIS_DIR_ABS"; cd ../lib; pwd)"
PIC_FRAME_PROG=$THIS_DIR/PictureFrame2020.py
source $THIS_DIR_ABS/activate

# X="$(basename "$PIC_FRAME_PROG")"
PIC_FRAME_LOG=/home/pi/.pf/logs/${THIS_FILE%.py}.log
PIC_FRAME_FILE_OPEN_LOG=/home/pi/.pf/dbg/${THIS_FILE%.py}_file_open.log
PYTHON="$(which python)"

REV="$(grep Revision /proc/cpuinfo)"
REV="${REV#*: }"

#------------------------------------------------------------------------------------------------------------
function usage() {
  cat <<EO_USAGE
  usage: $THIS_FILE [-hvfrt] [-d picture-dir] -a action

  Optional Command Line Switches:
    -a action. Valid actions: pic-stop, pic-start, pic-restart, pic-status, mqtt-start, x11-start
    -d picture-dir
    -f run in the foreground (to allow python debugging)
       add to python script: import pdb; pdb.set_trace()
       be sure X11 is running, e.g. by using command 'sudo systemctl start display-manager'
    -h print this page
    -v be more verbose.
    -r read additional command line parameters from file '$PF2020_OPTS_FNAME'
    -t trace file open activity using 'strace -e trace=openat -f -p 10015'
       Files opened are logged to $PIC_FRAME_FILE_OPEN_LOG

  Hints: 
    - You may pass additional command line options to PictureFrame2020.py by writing them to /home/pi/.pf/PictureFrame2020.cli_opts
      Run PictureFrame2020.py -h to learn more about available command arguments.
    - to identify the image crashing pi3d, use a command like:
      strace -e trace=openat -f -p 10015
    - check for 'out of memory' errors using the command 'dmesg -T' (search the pid of the python program in the dmesg output)


EO_USAGE
  exit 0
} # usage

#---------------------------------------------------------------------------------------------------
function echov() {
  [ "$VERBOSE" = true ] && echo "$*"
} # echov

#-----------------------------------------------------------------------------------------------------------------------
function pictureFrameStatus(){
  local PIC_FRAME_PIDS=$(pgrep -f "$(basename "$PIC_FRAME_PROG")")
  if [ -n "$PIC_FRAME_PIDS" ]; then 
    local P
    echo "$(basename "$PIC_FRAME_PROG") running with pids:"
    for P in $PIC_FRAME_PIDS; do
      local PIC_DIR="$(sed -e 's:\x00$::' -e 's:.*\x00::' /proc/$P/cmdline)" # extract last element of zero delimited elements
      printf "%6s: PIC_DIR=%s\n" "$P" "$PIC_DIR"
    done
    return 0
  else
    echo "$(basename "$PIC_FRAME_PROG") not running"
    return 1
  fi
} # pictureFrameStatus

#-----------------------------------------------------------------------------------------------------------------------
function killRunningPictureFrames() {
  local PIC_FRAME_PIDS=$(pgrep -f "$(basename "$PIC_FRAME_PROG")")
  local SUDO=""
  case "${REV:0:3}" in
    # RPi4
    c03) : ;&
    a03) SUDO="sudo "
  esac

  echov "+ killRunningPictureFrames()"
  if [ -n "$PIC_FRAME_PIDS" ]; then
    echov "+ ${SUDO}kill "$PIC_FRAME_PIDS
             ${SUDO}kill  $PIC_FRAME_PIDS
  fi
} # killRunningPictureFrames

#-----------------------------------------------------------------------------------------------------------------------
function pictureFrameStart() {
  local DIR="$1"
  # $!    - The PID of a backgrounded child process
  # $PPID - The process ID of the shell's parent.
  echov "+ pictureFrameStart(DIR='$DIR')"
  local RC PID PF2020_OPTS 
  local BACKGROUND_SWITCH="&"
  local REDIR_INSTR=">> $PIC_FRAME_LOG 2>&1"
  if [ "$RUN_FOREGROUND" = true ]; then
    BACKGROUND_SWITCH=""
    REDIR_INSTR=""
  fi

  # local SCREEN0_NOW_PLAYING_PID=$(pgrep --full 'Xvfb.*screen.0')
  local XVFB_ACTION="$(get_Xvfb_x11_server)"
  local START_NOW_PLAYING=False
  # no longer needed, moved to package pi3d-now-playing
  # if [ "$XVFB_ACTION" == restart ]; then
  #   # now-playing.py in local or mqtt_distribution mode running, with X11 Screen ID 0.
  #   # restart now-playing.py so PictureFrame.py can allocate X11 screen 0
  #   echo "+ sudo systemctl stop alexa-now-playing.service"
  #           sudo systemctl stop alexa-now-playing.service
  #   START_NOW_PLAYING=True
  #   local XVFB_PID="$(pgrep --full Xvfb)"
  #   while true; do
  #       if [ -z "$(pgrep --full Xvfb)" ]; then break; fi
  #       echo "+ sleep 2 # waiting for Xvfb PIDS '$XVFB_PID' to disappear"
  #               sleep 2
  #   done
  # fi

  if [ "$USE_PF2020_OPTS_FILE" = true -a -f "$PF2020_OPTS_FNAME" ]; then
    PF2020_OPTS="$(sed -e '/^#/ d' "$PF2020_OPTS_FNAME")"
    echo "INFO - additional command line options: '$PF2020_OPTS' (from '$PF2020_OPTS_FNAME')"
  else
    if [ "$USE_PF2020_OPTS_FILE" = false ]; then REASON="option -r not present"; else REASON="File '$PF2020_OPTS_FNAME' does not exist"; fi
    echo "INFO - no additional command line options added. ($REASON)"
    PF2020_OPTS=""
  fi


  case "${REV:0:3}" in
    a01) HW_MODEL=RPi2;&
    a02) HW_MODEL=RPi3
      local ACCELERATION="$(grep ^vc4 /proc/modules)" # RPi3 and modern acceleration cause error 'X11 needs to be running' when dtoverlay=vc4-fkms-v3d is enabled in /boot/config.txt
      if [ -n "$ACCELERATION" ]; then
        echo "WARNING - vc4 acceleration is enabled. This is known not to work with pi3d <= 2.38."
        echo "INFO - should you see errors like 'X11 needs to be running', remove [all]dtoverlay=vc4-fkms-v3d in /boot/config.txt"
      fi
      local CMD="cd '$(dirname "$PIC_FRAME_PROG")'; eval $PYTHON $PIC_FRAME_PROG -p '$DIR' $REDIR_INSTR $BACKGROUND_SWITCH"
      cd "$(dirname "$PIC_FRAME_PROG")"
      echo $CMD
      eval $PYTHON $PIC_FRAME_PROG -p "'$DIR'" $PF2020_OPTS $REDIR_INSTR $BACKGROUND_SWITCH
      RC=$?
      PID=$!
      ;;
    c03) : ;&
    a03) HW_MODEL=RPi4
      D="$(date '+%Y-%m-%d %H:%M')"
      eval echo $REDIR_INSTR
      eval echo $REDIR_INSTR
      eval echo $REDIR_INSTR
      # local DISPLAY_ID=$(get_next_free_x11_display_id)
      eval echo "$D - Starting Pictureframe... " $REDIR_INSTR
      if [ "$RUN_FOREGROUND" = true ]; then
        [ -f /home/pi/.pf/logs/PictureFrame2020.log ] && sudo chown pi:pi /home/pi/.pf/logs/PictureFrame2020.log
        echo "INFO - be sure x11 system is running (sudo systemctl start display-manager)"
        $PYTHON $PIC_FRAME_PROG -p "$DIR" $PF2020_OPTS
        RC=$?
      else
        set -x
        eval sudo xinit $PYTHON $PIC_FRAME_PROG -p "'$DIR'" $PF2020_OPTS -- :0 -s off -dpms -s noblank  $REDIR_INSTR $BACKGROUND_SWITCH
        RC=$?
        PID=$!
        set +x
      fi
      ;;
    *) echo "ERROR - implementation for revison '$REV' was not implemented"; exit 1;;
  esac

  if [ "$RC" -eq 0 ]; then echo "$DIR" > /home/pi/.pf/last_viewed/.pf-last-used-picture-dir.txt; fi

  if [ "$START_NOW_PLAYING" = True ]; then
    echo "+ sudo systemctl start alexa-now-playing.service"
            sudo systemctl start alexa-now-playing.service
  fi

  if [ $RC -eq 0 ]; then
    echo "INFO - $(basename "$PIC_FRAME_PROG") started, process running in background with pid $PID, check log file '$PIC_FRAME_LOG' for more info" >&2
  else
    echo "ERROR - something went wrong while trying to start $(basename "$PIC_FRAME_PROG")" >&2
    return
  fi

  if [ "$TRACE_OPEN_FILE" = true ]; then
    echo "INFO - should $(basename "$PIC_FRAME_PROG") crash, check $PIC_FRAME_FILE_OPEN_LOG for clues on file causing issues" >&2
    echo "+ strace -e trace=openat -A -t -f -p $PID -o $PIC_FRAME_FILE_OPEN_LOG &" >&2
            strace -e trace=openat -A -t -f -p $PID -o $PIC_FRAME_FILE_OPEN_LOG &  >&2
  fi
} # pictureFrameStart

#-----------------------------------------------------------------------------------------------------------------------
function x11Desktop() {
  local ACTION="$1" # mandatory. Use start or stop
  local LINK_TARGET
  # systemctl status display-manager
  echov "+ x11Desktop(ACTION='$ACTION')"
  case "${ACTION,,}" in
    start) LINK_TARGET=/lib/systemd/system/graphical.target                 ;;
    stop)  LINK_TARGET=/lib/systemd/system/multi-user.target                ;;
    *)     echo "ERROR - invalid action '$ACTION' in x11Desktop()"; return 1;;
  esac
  set -x
  sudo rm /etc/systemd/system/default.target
  sudo ln -s $LINK_TARGET /etc/systemd/system/default.target
  sudo systemctl $ACTION display-manager
  set +x
} # x11Desktop
#-----------------------------------------------------------------------------------------------------------------------
function mqttOperation() {
  local ACTION="$1"
  echo "PYTHONPATH=$PYTHONPATH"
  $PYTHON $THIS_DIR_ABS/mqttForHyperion.py
} # mqttOperation

#-----------------------------------------------------------------------------------------------------------------------
function now_playing() {
  local ACTION="$1" # mandatory, use one of 'start' 'stop'
  # pgrep 'Xvfb|chromedriver|chromium-browser|now-playing.py'
  case "$ACTION" in
    start|restart|status)
      systemctl $ACTION alexa-now-playing
      ;;
    stop)
      local PIDLIST RETRY_COUNT=10
      while true; do
        PIDLIST="$(pgrep 'Xvfb|chromedriver|chromium-browser|now-playing.py')"
        if [ -z "$PIDLIST" -o "$RETRY_COUNT" -le 0 ]; then break; fi
        kill $PIDLIST
        sleep 2
        RETRY_COUNT=$((RETRY_COUNT-1))
      done
      if [ "$RETRY_COUNT" -le 0 ]; then exit 1; else exit 0; fi
      ;;
    *)
      echo "ERROR - now_playing() - unexpected action '$ACTION'"
      exit 1
      ;;
  esac
}

#-----------------------------------------------------------------------------------------------------------------------
function get_Xvfb_x11_server() {
  local F P RESULT="no restart" INFO=""
  local N=$(find /tmp/.X11-unix/ -type s|wc -l)
  if [ "$N" -gt 0 ]; then
    while IFS=: read F P; do
      F="$(basename "$F")"
      C="$(ps -hp ${P//[[:blank:]]/} -o comm)"
      if [ "$C" == Xvfb -a "$F" == X0 ]; then
        RESULT=restart
        INFO+="INFO - get_Xvfb_x11_server() - $C is running as X11 server :${F:1}, Xvfb $RESULT required"
      fi
    done < <(sudo fuser /tmp/.X11-unix/* 2>&1)
  fi
  [ -n "$INFO" ] && echo "$INFO" >&2
  echo "$RESULT"
} # get_Xvfb_x11_server

#-----------------------------------------------------------------------------------------------------------------------
##  __  __       _
## |  \/  |     (_)
## | \  / | __ _ _ _ __
## | |\/| |/ _` | | '_ \
## | |  | | (_| | | | | |
## |_|  |_|\__,_|_|_| |_|
##

PF2020_OPTS_FNAME=/home/pi/.pf/PictureFrame2020.cli_opts
VERBOSE=false
ACTION=uninitialized
PICTURE_DIR=uninitialized
TRACE_OPEN_FILE=false
RUN_FOREGROUND=false
USE_PF2020_OPTS_FILE=false
while getopts a:d:fhrtv ARG; do
  case "$ARG" in
    a) ACTION="$OPTARG"                     ;;
    d) PICTURE_DIR="$OPTARG"                ;;
    f) RUN_FOREGROUND=true                  ;;
    h) usage; exit 0                        ;;
    r) USE_PF2020_OPTS_FILE=true            ;;
    t) TRACE_OPEN_FILE=true                 ;;
    v) VERBOSE=true;V_LEVEL=$((V_LEVEL + 1));;
    *) echo "ERROR - invalid option '$ARG'"; exit 1;
  esac
done
shift $((OPTIND-1))

if [ "$ACTION" = uninitialized ]; then echo "ERROR - Option -a is mandatory."; exit 1; fi
if [ "$ACTION" = pic-start -a "$PICTURE_DIR" = uninitialized ]; then echo "ERROR - option -d is mandatory for '-a pic-start'."; exit 1; fi


case "$ACTION" in
  pic-status)    pictureFrameStatus; exit $?;;
  pic-stop)      killRunningPictureFrames;;
  pic-start)     killRunningPictureFrames; if [ "$RUN_FOREGROUND" = false ]; then x11Desktop stop; fi; pictureFrameStart $PICTURE_DIR;;
  pic-restart)   echo not implemented;;
  x11-start)     killRunningPictureFrames; x11Desktop start;;
  mqtt-start)    mqttOperation;;
  uninitialized) echo "ERROR - option -a is mandatory"; usage; exit 1;;
  *) echo "ERROR - action '$ACTION' in option '-a $ACTION' is not recognized";;
esac
