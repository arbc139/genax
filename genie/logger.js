const winston = require('winston');

const logger = new (winston.Logger)({
  levels: {
    info: 0,
    warn: 1,
    error: 2,
  },
  transports: [
    new (winston.transports.Console)(),
    /**
     * new (winston.transports.File)({ filename: 'somefile.log' }),
     * ...so and on...
     */
  ]
});

module.exports = logger;
