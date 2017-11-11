const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all GENE SCORES LIMIT IS 10 DUE TO MEM LIMIT.
router.get('/', (req, res) => {
  database.query('SELECT * FROM GENE_SCORE LIMIT 10')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find diseases by keyword.
router.get('/:j_id/:net_id', (req, res) => {
  const query = `SELECT * FROM GENE_SCORE WHERE J_ID = ${req.params.j_id} AND \
      NET_ID = ${req.params.net_id} ORDER BY DEGREE DESC`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

