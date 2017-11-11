const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all IDs and keys
router.get('/', (req, res) => {
  database.query('SELECT HGNC_ID,SYMBOL FROM GENE LIMIT 10')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find ID with corresponding key
router.get('/:hgnc_id/', (req, res) => {
  const HgncId = `"${req.params.hgnc_id}"`;
  const query = `SELECT HGNC_ID, SYMBOL FROM GENE WHERE HGNC_ID = ${HgncId};`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

