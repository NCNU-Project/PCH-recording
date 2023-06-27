# PCH-recording

## Prepare Deploy environment

- [ubuntu](docs/deploy-on-ubuntu.md)
- [almalinux](docs/deploy-on-almalinux.md)

## How to deploy this project

1. clone this repo: `git clone https://github.com/efficacy38/PCH-recording.git`
2. cd the working directory: `cd PCH-recording/demo`
3. please change the PUBLIC_IPV4 in docker-compose.yml and rtpengine.conf to your current public IP which is ipv4
   - `docker-compose.yml`:
   - the one is under kamailio's environments
   - the other one is under kamailio's port mapping
   - change `163.22.22.67:5060:5060/udp` to "your_IPV4:5060:5060/udp"
   - `rtpengine.conf`:
   - this one is at the field `interface`, the format is `private_IP!public_IP`, so just edit the `public_IP`'s field
4. start the application with: `docker-compose up`

## Add the users for kamailio

- get into kamailio container: `docker exec -it demo_kamailio_1 /bin/bash`
- edit kamailio config file: `vim /etc/kamailio/kamctlrc`
  - uncomment and change `SIP_DOMAIN` to k8s kamailio this machine's public IP(IPv4)
  - uncomment `DBENGINE`
  - uncomment `DBHOST` and change it to `mysqldb`(which is the service that is defined at `docker-compose.yml`)
  - uncomment `DBPORT`, `DBNAME`
  - uncomment `DBRWUSER`, `DBRWPW`, `DBROUSER`, `DBROPW` to your db credentials(which is `MYSQL_USER`, `MYSQL_PASSWORD`, defined mysqldb's environment under `docker-compose.yml`)
  - add user
    - kamctl add $username $password

## application

- SIP server: `PUBLIC_IPV4:5060`
- recording files serve server: `PUBLIC_IPV4:8080`
