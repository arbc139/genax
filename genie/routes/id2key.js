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
router.get('/:j_id/', (req, res) => {
  const jobId = `"${req.params.j_id}"`;
  const query = `SELECT J_ID, J_KEY FROM JOB WHERE J_ID = ${jobId};`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

