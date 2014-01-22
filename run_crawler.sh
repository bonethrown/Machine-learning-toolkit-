#!/bin/bash
# Description of script
 
# Display usage if no parameters given
if [[ -z "$@" ]]; then
  echo " ${0##*/} <input> <working dir> - please input crawler name"
  exit
fi
 
### Variables ###
SHELL=/bin/bash
MAILTO=/var/mail/dev
HOME=/home/dev/kk_cosme/cosme
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/jvm/java-7-oracle/bin



EPOCH=$((`date +"%m-%d-%y"`))
CRAWLER_NAME=$1
WORKING_DIR=$2
LOG_FOLDER="/tmp/log_scrapy_$CRAWLER_NAME-$EPOCH.log"
LOCK_FILE="/tmp/$CRAWLER_NAME-$EPOCH.TXT"
CMD_RUN="scrapy crawl --pidfile=$LOCK_FILE --logfile=$CRAWLER_NAME-crawl-$EPOCH.LOG  $CRAWLER_NAME"

cd $WORKING_DIR
echo "running $1 in $2 date:%EPOCH"
echo "command: $CMD_RUN"

scrapy crawl --pidfile=$LOCK_FILE --logfile=$LOG_FOLDER  $CRAWLER_NAME


# Required program(s)
#req_progs=(prog1 prog2)
#for p in ${req_progs[@]}; do
#  hash "$p" 2>&- || \
#  { echo >&2 " Required program \"$p\" not installed."; exit 1; }
#done
 


# Text color variables
txtund=$(tput sgr 0 1)          # Underline
txtbld=$(tput bold)             # Bold
bldred=${txtbld}$(tput setaf 1) #  red
bldblu=${txtbld}$(tput setaf 4) #  blue
bldwht=${txtbld}$(tput setaf 7) #  white
txtrst=$(tput sgr0)             # Reset
info=${bldwht}*${txtrst}        # Feedback
pass=${bldblu}*${txtrst}
warn=${bldred}*${txtrst}
ques=${bldblu}?${txtrst}

