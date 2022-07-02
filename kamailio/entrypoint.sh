#!/bin/bash
# Set default settings, pull repository, build
# app, etc., _if_ we are not given a different
# command.  If so, execute that command instead.
set -e

# Default values
: ${PID_FILE:="/var/run/kamailio.pid"}
: ${KAMAILIO_ARGS:="-DD -E -f /etc/kamailio/kamailio.cfg -P ${PID_FILE}"}

# confd requires that these variables actually be exported
export PID_FILE

# Make dispatcher.list exists
mkdir -p /data/kamailio
touch /data/kamailio/dispatcher.list

: ${PRIVATE_IPV4:="$(netdiscover -field privatev4 ${PROVIDER})"}
: ${PUBLIC_IPV4:="$(netdiscover -field publicv4 ${PROVIDER})"}
: ${PUBLIC_HOSTNAME="$(netdiscover -field hostname ${PROVIDER})"}

cat <<ENDHERE >/data/kamailio/local.k
alias=${PUBLIC_IPV4}
listen=udp:${PRIVATE_IPV4}:5060 advertise ${PUBLIC_IPV4}:5060
listen=udp:${PRIVATE_IPV4}:5080
ENDHERE

# Runs kamaillio, while shipping stderr/stdout to logstash
exec /usr/sbin/kamailio $KAMAILIO_ARGS $*
