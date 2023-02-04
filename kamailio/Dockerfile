FROM debian:buster

RUN apt-get update && \
    apt-get install -y curl procps gnupg2 sngrep jq && \
    apt-get clean

# Install kamailio
RUN curl -qO http://deb.kamailio.org/kamailiodebkey.gpg && \
    apt-key add kamailiodebkey.gpg && \
    echo "deb http://deb.kamailio.org/kamailio56 buster main\ndeb-src http://deb.kamailio.org/kamailio56 buster main" > /etc/apt/sources.list.d/kamailio.list
RUN apt-get update &&  apt-get install -y kamailio kamailio-json-modules kamailio-utils-modules kamailio-extra-modules kamailio-nth kamailio-tls-modules kamailio-mysql-modules default-libmysqlclient-dev gnutls-bin && apt-get clean

# Download netdiscover
RUN curl -qL -o /usr/bin/netdiscover https://github.com/CyCoreSystems/netdiscover/releases/download/v1.2.5/netdiscover.linux.amd64
RUN chmod +x /usr/bin/netdiscover

RUN curl -qL -o /usr/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /usr/bin/wait-for-it.sh

# Install config and templates
ADD config /etc/kamailio
# ADD dispatcher.list /data/kamailio/dispatcher.list

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
# ENTRYPOINT ["kamailio", "-DD", "-E", "-f", "/etc/kamailio/kamailio.cfg"]

CMD []
