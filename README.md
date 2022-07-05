# PCH-recording

## test environment
- OS: Ubuntu 20.04
- docker engine version: `Docker version 20.10.17, build 100c701`
- docker compose version: `docker-compose version 1.25.0, build unknown`

## Pre-Request
### install docker and docker-compose
- follow the instruction of [docker's official instruction](https://docs.docker.com/engine/install/ubuntu/)
    1. Set up the repository
    ```
    sudo apt-get update
    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```
    2. Add Docker’s official GPG key:
    ```
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```
    3. Use the following command to set up the repository:
    ```
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
    4. install docker engine and docker compose
    ```
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose
    ```
- install the rtpengine kernel module to optimize the performance of RTP packet forwarding
    1. go to the clean work directory: `cd /tmp`
    2. get the kernel module: `wget http://ms15.voip.edu.tw/~jerry/build.tar.gz`
    3. extract the pre-build deb packets: `tar -zxvf build.tar.gz`
    4. change to the directory that contain the pre-build deb: `cd ./build/rtpengine`
    5. install the kernel module: `sudo apt install ./ngcp-rtpengine-kernel-dkms_10.5.0.0+0~mr10.5.0.0_all.deb ./ngcp-rtpengine-iptables_*`
    6. enable the kernel module: `sudo modprobe xt_RTPENGINE`
        - check whether the module is installed: `lsmod  | grep xt_RTPENGINE`
            - if there are prompt with xt_RTPENGINE, then it is install successfully

## How to deploy this project
1. clone this repo: `git clone https://github.com/efficacy38/PCH-recording.git`
2. cd the working directory: `cd PCH-recording/demo`
3. please change the PUBLIC_IPV4 in docker-compose.yml and rtpengine.conf to your current public IP which is ipv4
    - `docker-compose.yml`: this one is under kamailio's environments
    - `rtpengine.conf`: this one is at the field `interface`
4. start the application with: `docker-compose up`

## Add the users for kamailio
- get into kamailio container: `docker exec -it demo_kamailio_1 /bin/bash`
- edit kamailio config file: `vim /etc/kamailio/kamctlrc`
    - uncomment and change `SIP_DOMAIN` to k8s kamailio this machine's public IP(IPv4)
    - uncomment `DBENGINE`
    - uncomment `DBHOST` and change it to `mysqldb`(which is the service that is defined at `docker-compose.yml`)
    - uncomment `DBPORT`, `DBNAME`
    - uncomment `DBRWUSER`, `DBRWPW`, `DBROUSER`, `DBROPW` to your db credentials(which is `MYSQL_USER`, `MYSQL_PASSWORD`, defined mysqldb's environment under `docker-compose.yml`)

## application
- SIP server: `PUBLIC_IPV4:5060`
- recording files serve server: `PUBLIC_IPV4:8080`
