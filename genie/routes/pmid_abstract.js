const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all ARTICLES LIMIT IS 10 DUE TO MEM LIMIT.
router.get('/', (req, res) => {
  database.query('SELECT ABSTRACT FROM PMID_CONTENT LIMIT 10')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find all title of ARTICLES RELATED TO THE GENE IN THE WORK
router.get('/:pmid', (req, res) => {
  const query = `SELECT ABSTRACT FROM PMID_CONTENT WHERE PMID = ${req.params.pmid};`
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

