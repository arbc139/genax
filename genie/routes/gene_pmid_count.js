const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all ARTICLES LIMIT IS 10 DUE TO MEM LIMIT.
router.get('/', (req, res) => {
  database.query('SELECT count(*) FROM PMID_CONTENT_2 LIMIT 10')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find all title of ARTICLES RELATED TO THE GENE IN THE WORK
router.get('/:j_id/:hgnc_id', (req, res) => {
  const query = `SELECT DISTINCT COUNT(*) FROM GENE_PMID WHERE J_ID = ${req.params.j_id} AND \
        HGNC_ID = ${req.params.hgnc_id};`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

