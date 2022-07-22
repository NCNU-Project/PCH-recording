FROM debian:bullseye

MAINTAINER Jerry Drung "efficacy38@gmail.com"

RUN apt-get update \
  && apt-get install -y wget curl \
  && TMP_DIR=$(mktemp -d) \
  && wget http://ms15.voip.edu.tw/~jerry/new-build.tar.gz -O "$TMP_DIR/build.tar.gz" \
  && tar -zxvf "$TMP_DIR/build.tar.gz" -C $TMP_DIR \
  && apt-get install -y $TMP_DIR/ngcp-rtpengine-daemon*.deb $TMP_DIR/ngcp-rtpengine-recording-daemon*.deb \
  && rm -rf $TMP_DIR \
  && rm -rf /var/lib/apt/* \
  && rm -rf /var/lib/cache/* \
  && rm -Rf /var/log/* \
  && rm -Rf /usr/local/src/* \
  && rm -Rf /var/lib/apt/lists/* 
  # && rm -rf /var/lib/dpkg/* \

VOLUME ["/tmp"]

EXPOSE 23000-32768/udp 22222/udp

# Download netdiscover
RUN curl -qL -o /usr/bin/netdiscover https://github.com/CyCoreSystems/netdiscover/releases/download/v1.2.5/netdiscover.linux.amd64
RUN chmod +x /usr/bin/netdiscover

COPY ./entrypoint.sh /entrypoint.sh

COPY ./rtpengine.conf /etc/rtpengine

ENTRYPOINT ["/entrypoint.sh"]

CMD ["rtpengine"]
