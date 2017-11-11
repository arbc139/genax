const yargs = require('yargs');

module.exports = yargs
  .option('user', {
    default: '',
  })
  .option('password', {
    default: '',
  }).argv;
