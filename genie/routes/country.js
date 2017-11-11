const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all countries
router.get('/', (req, res) => {
  database.query('SELECT * FROM COUNTRY')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find diseases by keyword.
router.get('/:keyword/', (req, res) => {
  const keywordAll = `"${req.params.keyword}"`;
  const keywordWord = `" ${req.params.keyword}"`;
  const keywordStart = `"^${req.params.keyword}"`;
  const query = `(SELECT * FROM COUNTRY WHERE C_NAME REGEXP ${keywordStart}) \
      UNION (SELECT * FROM COUNTRY WHERE C_NAME REGEXP ${keywordWord}) \
      UNION (SELECT * FROM COUNTRY WHERE C_NAME REGEXP ${keywordAll})`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

