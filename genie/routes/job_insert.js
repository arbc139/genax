const express = require('express');
const util = require('util');

const database = require('../database');
const logger = require('../logger');
var keygen = require("keygenerator");

const router = express.Router();

// (POST) Insert the job.
router.post('/', (req, res) => {
  /*const today = new Date();
  const date = util.format(
      '%d-%d-%d', today.getFullYear(), today.getMonth() + 1, today.getDate());
  const time = util.format(
      "%d:%d:%d", today.getHours(), today.getMinutes(), today.getSeconds());*/
  let tempQuery = req.body.query.replace(/["]+/g, '')
  const searchQuery = `"${tempQuery}"`;
  //const jobStartTime = `"${date} ${time}"`;
  const jobKey = `"${keygen._(
      {
          forceUppercase : true,
          length : 5,
          chars : true,
          sticks : false,
          numbers : false,
          specials : false
      }
  )}"`;
  logger.info('req: ', req.body);
  const startDate = `"${req.body.start_date}"`;
  const endDate = `"${req.body.end_date}"`;
  const nodeSize = `"${req.body.node_size}"`;
  const email = `"${req.body.email}"`;
  /*const I = `"${req.body.I}"`;
  const N = `"${req.body.N}"`;
  const T = `"${req.body.T}"`;
  const C = `"${req.body.C}"`;
  const U = `"${req.body.U}"`;
  const M = `"${req.body.M}"`;
  const D = `"${req.body.D}"`;
  const S = `"${req.body.S}"`;
  const EM = `"${req.body.EM}"`;*/
  const MIN_SUP = `"${req.body.MIN_SUP}"`;
  const MAX_PVAL = `"${req.body.MAX_PVAL}"`;
  const MIN_NODE_SUP = `"${req.body.MIN_NODE_SUP}"`;
  const COOC_EM = `"${req.body.COOC_EM}"`;
  logger.info('Search query: ', searchQuery);
  logger.info('Job key: ', jobKey);
  //logger.info('Job start time: ', jobStartTime);
  logger.info('Job start date: ', startDate);
  logger.info('End date: ', endDate);
  logger.info('Node size: ', nodeSize);
  logger.info('Email: ', email);
  /*const query = `INSERT INTO JOB (QUERY, J_KEY, START_DATE,
                                  END_DATE, NODE_SIZE, EMAIL,\
                                I, N, T, C, U, M, D, S, EM) \
                 VALUES (${searchQuery}, ${jobKey}, \
                     ${startDate}, ${endDate}, ${nodeSize}, ${email},\
                    ${I}, ${N}, ${T}, ${C}, ${U}, ${M}, ${D}, ${S}, ${EM});`;*/
  const query = `INSERT INTO JOB (QUERY, J_KEY, START_DATE,
                                  END_DATE, NODE_SIZE, EMAIL,\
                                MIN_SUP, MAX_PVAL, MIN_NODE_SUP,COOC_EM) \
                 VALUES (${searchQuery}, ${jobKey}, \
                     ${startDate}, ${endDate}, ${nodeSize}, ${email},\
                    ${MIN_SUP}, ${MAX_PVAL}, ${MIN_NODE_SUP}, ${COOC_EM});`;
  database.query(query)
      .catch(err => {
        logger.error(err);
      })
      .then(rows => {
      res.send(rows);
      });
});

module.exports = router;

