# Backoffice
Genax Web Frontend Application

## Framework
`Vue.js`

## Build Setup

``` bash
# install dependencies
$ npm install

# serve with hot reload at localhost:8080
$ npm run dev

# build for production with minification
$ npm run build

# build for production and view the bundle analyzer report
$ npm run build --report

# run unit tests
$ npm run unit

# run e2e tests
$ npm run e2e

# run all tests
$ npm test
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## How To Build In Server
``` bash
# You have to execute all command on normal user.
# Do not execute each line on sudo
# If you pull from repo and build on sudo account,
# Gene Score won't work

$ npm install
$ npm run build

# If 'serve' is not installed, install it globally.
$ npm install -g serve
$ serve -s dist
# Backoffice will listening a request in '5000' port...

$ sudo serve -s dist -p 80
# Backoffice will listening a request in '80' port...
```

## How To Make a Docker Image
```bash
# Make backoffice images
$ docker build -t arbc139/genax-front:1.0.0 .
```
