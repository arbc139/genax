const express = require('express');

const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) Find all ARTICLES LIMIT IS 10 DUE TO MEM LIMIT.
router.get('/', (req, res) => {
  database.query('SELECT * FROM PMID_CONTENT_2 LIMIT 10')
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});

// (GET) Find all title of ARTICLES RELATED TO THE GENE IN THE WORK
router.get('/:j_id/:hgnc_id', (req, res) => {
  const query = `SELECT A.PC_ID,A.PMID,A.TITLE FROM PMID_CONTENT_2 A WHERE PMID IN\
  (SELECT * FROM \
   (SELECT PMID FROM \
   GENE_PMID B WHERE J_ID = ${req.params.j_id} AND \
   HGNC_ID = ${req.params.hgnc_id} ORDER BY B.PMID DESC  \
  ) AS TMP\
 )ORDER BY A.PMID DESC`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
        res.send(rows);
      });
});


// (GET) Find all title of ARTICLES RELATED TO THE GENE IN THE WORK
//IN THIS VERSION YOU CAN LIMIT START AND  STEP
router.get('/:j_id/:hgnc_id/:retstart/:retmax', (req, res) => {
  const query = `SELECT A.PC_ID,A.PMID,A.TITLE FROM PMID_CONTENT_2 A WHERE PMID IN\
    (SELECT PMID FROM \
    GENE_PMID B WHERE J_ID = ${req.params.j_id} AND \
    HGNC_ID = ${req.params.hgnc_id} \
    )\
    ORDER BY A.PMID DESC LIMIT ${req.params.retstart}, ${req.params.retmax} `;
  database.query(query)
      .catch(err => {
        logger.error('Failed to find all articles.');
      })
      .then(rows => {
        res.send(rows);
      });
});
module.exports = router;

