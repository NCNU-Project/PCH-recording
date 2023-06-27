# Prepare environment on ubuntu 20.04 with RTPEngine Kernel Module

## install docker and docker-compose

> **Note**
>
> follow the instruction of [docker's official instruction](https://docs.docker.com/engine/install/ubuntu/)

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

## install the rtpengine kernel module to optimize the performance of RTP packet forwarding

1. go to the clean work directory: `cd /tmp`
2. get the kernel module: `wget http://ms15.voip.edu.tw/~jerry/new-build.tar.gz`
3. extract the pre-build deb packets: `tar -zxvf new-build.tar.gz`
4. install the kernel module: `sudo apt install ./ngcp-rtpengine-kernel-dkms*.deb ./ngcp-rtpengine-iptables_*`
5. enable the kernel module: `sudo modprobe xt_RTPENGINE`
   - check whether the module is installed: `lsmod  | grep xt_RTPENGINE`
     - if there are prompt with xt_RTPENGINE, then it is install successfully
