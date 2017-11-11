
const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

router.get('/', (req, res) => {
  res.send('Root');
});

// (GET) Find all jobs.
router.get('/jobs', (req, res) => {
  database.query('SELECT * FROM JOB')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find one job by ID.
router.get('/jobs/:job_num/', (req, res) => {
  const query = `SELECT * FROM JOB WHERE J_ID = ${req.params.job_num}`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;
