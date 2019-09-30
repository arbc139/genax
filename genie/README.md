# Genie
Gene analyzer 서비스를 제공하는 REST API server.

## Framework
`node.js` `express`

## Build setup
`npm`과 `node`를 설치해주세요.

### Mac
``` bash
$ brew install node
```
### Linux(ubuntu)
``` bash
$ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
$ sudo apt-get install -y nodejs
```

그리고 `npm`을 이용하여 package들을 설치해주세요.

### Install packages
``` bash
$ npm install
```

## Start
다음 command로 서버를 실행시킬 수 있습니다.
``` bash
# Database password will be ''.
$ npm start -- --user="DBUser"
# Run server with database password...
$ npm start -- --user="DBUser" --password="DBPassword"
```

## Database
`MySQL`을 사용하고 있습니다. \
Database connection 설정은 `config/`와 `database.js` 에서 관리합니다.

## Docker
다음 command로 Docker Image를 생성할 수 있습니다.
```bash
$ docker build -t arbc139/genax-back:1.0.0 .
```

## SSL
directory 'bin/ssl' is https related.
Please make private key and update public key before build up.
```bash
# Make private key
openssl genrsa -out bin/ssl/key.pem 1024
# Make public key
openssl req -x509 -new -key bin/ssl/key.pem > bin/ssl/cert.pem
```
