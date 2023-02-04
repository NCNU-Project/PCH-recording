ARG RTPENGINE_VER=mr11.2.1.1

FROM debian:bullseye AS builder

ARG RTPENGINE_VER
WORKDIR /build
RUN apt-get update && \
    apt-get install -y debhelper-compat default-libmysqlclient-dev gperf libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev  libbcg729-dev libbencode-perl libcrypt-openssl-rsa-perl libcrypt-rijndael-perl libcurl4-openssl-dev libdigest-crc-perl libdigest-hmac-perl libevent-dev libglib2.0-dev libhiredis-dev libio-multiplex-perl libio-socket-inet6-perl libiptc-dev libjson-glib-dev libjson-perl libmosquitto-dev libnet-interface-perl libopus-dev libpcap0.8-dev libpcre3-dev libsocket6-perl libspandsp-dev libssl-dev libswresample-dev libsystemd-dev libtest2-suite-perl libwebsockets-dev libxmlrpc-core-c3-dev markdown python3 python3-websockets zlib1g-dev libxtables-dev git && \
    git clone --branch=${RTPENGINE_VER} https://github.com/sipwise/rtpengine.git && \
    cd rtpengine && \
    dpkg-checkbuilddeps && \
    dpkg-buildpackage  --no-sign

FROM debian:bullseye
COPY --from=builder /build/ngcp-* /build/
RUN apt-get update && \
    apt-get install -y /build/ngcp*.deb curl

VOLUME ["/tmp"]
EXPOSE 23000-32768/udp 22222/udp

# Download netdiscover
RUN curl -qL -o /usr/bin/netdiscover https://github.com/CyCoreSystems/netdiscover/releases/download/v1.2.5/netdiscover.linux.amd64
RUN chmod +x /usr/bin/netdiscover

COPY ./entrypoint.sh /entrypoint.sh

COPY ./rtpengine.conf /etc/rtpengine.conf

ENTRYPOINT ["/entrypoint.sh"]

CMD ["rtpengine"]
