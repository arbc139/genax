const express = require('express');

const argv = require('../argv');
const database = require('../database');
const logger = require('../logger');

const router = express.Router();

// (GET) download certain type of files for job j_id and j_key
router.get('/:j_id/:j_key/:f_type', (req, res) => {

  const homeDir = `/home/${argv.user}/Capstone-2017-2/gena/files/`;

  const jId = `${req.params.j_id}`;
  const jKey = `${req.params.j_key}`;
  const fType = `${req.params.f_type}`;
  switch(fType){
      case '0':
        fileName = '_edgeAsso.csv';
        break;
      case '1':
        fileName = '_edgeCooc.csv';
        break;
      case '2':
        fileName = '_SingleOccurringNode.csv';
        break;
      case '3':
        fileName = '_GeneAssociation.csv';
        break;
      case '4':
        fileName = '_GeneAssociationSingleNode.csv';
        break;
      case '5':
        fileName = '_GeneCoOccurence.csv';
        break;
      case '6':
        fileName = '_GeneCoOccurenceSingleNode.csv';
        break;
      default:
      fileName = '_edgeAsso.csv';
  }
  res.download(`${homeDir}${jId}/${jKey}${fileName}`); // Set disposition and send it.
});

module.exports = router;
