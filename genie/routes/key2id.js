const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all IDs and keys
router.get('/', (req, res) => {
  database.query('SELECT J_ID,J_KEY FROM JOB')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find ID with corresponding key
router.get('/:j_key/', (req, res) => {
  const jobKey = `"${req.params.j_key}"`;
  const query = `SELECT J_ID, J_KEY FROM JOB WHERE J_KEY = ${jobKey};`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

