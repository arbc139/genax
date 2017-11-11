const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all diseases.
router.get('/', (req, res) => {
  database.query('SELECT * FROM DISEASE')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find diseases by keyword.
router.get('/:keyword/', (req, res) =>  {
  const keywordAll = `"${req.params.keyword}"`;
  const keywordWord = `" ${req.params.keyword}"`;
  const keywordStart = `"^${req.params.keyword}"`;
  const query = `(SELECT * FROM DISEASE WHERE DIS_NAME REGEXP ${keywordStart}) \
      UNION (SELECT * FROM DISEASE WHERE DIS_NAME REGEXP ${keywordWord}) \
      UNION (SELECT * FROM DISEASE WHERE DIS_NAME REGEXP ${keywordAll}) \
      LIMIT 30`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

module.exports = router;

