
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const express = require('express');
const logger = require('morgan');
const path = require('path');

const database = require('./database');

const app = express();

// View engine setup.
// TODO(dykim): Remove these engines when we don't use any views.
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// Parsers, Loggers setup.
app.use(cors());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

module.exports = app;
