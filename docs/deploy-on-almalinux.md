# Deploy Kamailio and RTPEngine suit on Almalinux 8 with RTPEngine Kernel Module

> **Warning**
>
> Please be careful about kernel module and rtpengine's version

[scrawled note about the compilation](https://www.notion.so/efficacy38/Build-VoIP-stuff-a851e8021b7d428ea287567429a5b484?pvs=4)

## Build RTPEngine Kernel Module

1. before start build kernel stuff, update your system first:

   ```bash
   dnf -y update
   # if dnf update your kernel, then you may get wrong when build the kernel module(loss some kernel src)
   reboot now
   ```

2. prepare the building environment:

   ```bash
   dnf -y install iptables-services iptables-devel
   systemctl start iptables.service
   iptables -F
   service iptables save

   # check iptables status
   systemctl status iptables.service
   # install epel
   dnf -y install https://download.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
   dnf -y install yum-utils
   yum-config-manager --enable powertools
   # install rpm fusion for more packages
   dnf install -y --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
   dnf install -y ffmpeg ffmpeg-devel
   # check the ffmpeg
   rpm -qi ffmpeg

   # install build essential
   dnf -y install gcc gcc-c++ kernel-devel make

   # install the rtpengine dependicy
   dnf -y install git gcc git glib2-devel gperf hiredis hiredis-devel iptables-devel json-c-devel json-glib json-glib-devel libcurl libcurl-devel libevent-devel libpcap-devel libwebsockets-devel mariadb mariadb-devel openssl openssl-devel pcre pcre-devel perl-IPC-Cmd redis spandsp-devel wget xmlrpc-c xmlrpc-c-devel zlib zlib-devel

   # install codec
   dnf -y install opus-1.3-0.4.beta.el8.x86_64 opus-devel-1.3-0.4.beta.el8.x86_64

   # important!!
   # important!!
   # important!! maybe okay.com.mx is not the best practice of the rpm source
   # maybe install bcg729 at some "official" repository,
   # please try this "dnf -y install bcg729 bcg729-devel"
   dnf -y install http://repo.okay.com.mx/centos/8/x86_64/release/bcg729-devel-1.0.4-5.el8.x86_64.rpm http://repo.okay.com.mx/centos/8/x86_64/release/bcg729-1.0.4-5.el8.x86_64.rpm
   ```

3. compile rtpengine Kernel Module, manage your `RTPENGINE_VER` carefully

   ```bash
   # specify the rtpengine version
   export RTPENGINE_VER=mr11.2.1.1

   # checkout rtpengine
   cd /usr/src
   git clone --branch=${RTPENGINE_VER} https://github.com/sipwise/rtpengine.git rtpengine

   # compile daemon
   cd /usr/src/rtpengine/daemon/
   make

   # install daemon
   cp -fr rtpengine /usr/sbin/rtpengine
   cp -fr rtpengine /usr/local/bin/rtpengine

   # compile the itpables extension
   cd /usr/src/rtpengine/iptables-extension
   make all

   # install the library
   cp -fr libxt_RTPENGINE.so /usr/lib64/xtables/.

   # compile the kernel module xt_RTPENGINE
   cd /usr/src/rtpengine/kernel-module
   make

   # install the kernel module
   cp -fr xt_RTPENGINE.ko /lib/modules/`uname -r`/xt_RTPENGINE.ko
   depmod -a
   # load the kernel module
   modprobe -v xt_RTPENGINE
   ```

4. check kernel module is installed

   ```bash
   # check the kernel module is load, and make kernel module load whenever on boot
   lsmod | grep xt_RTPENGINE

   # persist this kernel module's status
   echo "# load xt_RTPENGINE module" | sudo tee -a /etc/modules-load.d/rtpengine.conf
   echo "xt_RTPENGINE" | sudo tee -a /etc/modules-load.d/rtpengine.conf
   ```

5. (optional) save all your compiled files to ms15

   ```bash
   cd /usr/src/
   # create a kernel version file
   uname -r > rtpengine/kernel_version
   tar -zcvf build_rtpengine_almaLinux.tar.gz rtpengine
   scp -P 3261 build_rtpengine_almaLinux.tar.gz jerry@ms15.voip.edu.tw:~/www/archive/
   ```

## Install Kernel Module from your previous builded binary

> **Warning**
>
> Please be careful about kernel version difference between build environment and your current deploy envrionment

1. install the RTPEngine kernel module

   ```bash
   dnf update -y
   dnf install -y wget git
   # install the kernel module
   cd /usr/src
   # checkout the prebuild source code
   sudo wget http://ms15.voip.edu.tw/~jerry/archive/build_rtpengine_almaLinux.tar.gz
   sudo tar -zxvf build_rtpengine_almaLinux.tar.gz

   if [ "$(cat /usr/src/rtpengine/kernel_version)" != "$(uname -r)" ]; then
     printf "\n\nkernel version unmatch, difference between kernel may cause unpredictable bug!!\n\n"
   else
     cd /usr/src/rtpengine/kernel-module
     sudo cp -fr xt_RTPENGINE.ko /lib/modules/`uname -r`/xt_RTPENGINE.ko
     sudo depmod -a
     # load the kernel module
     sudo modprobe -v xt_RTPENGINE
     # check the kernel module is load
     lsmod | grep xt_RTPENGINE

     # persist this kernel module's status
     echo "# load xt_RTPENGINE module" | sudo tee -a /etc/modules-load.d/rtpengine.conf
     echo "xt_RTPENGINE" | sudo tee -a /etc/modules-load.d/rtpengine.conf    lsmod | grep xt_RTPENGINE
   fi
   ```

2. install docker runtime
   ```bash
   # install docker at alma linux
   dnf --refresh update
   dnf upgrade
   dnf -y install yum-utils
   yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   systemctl enable docker
   systemctl start docker
   systemctl status docker
   ```
