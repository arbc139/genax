const logger = require('../logger');
const parseString = require('xml2js').parseString;
const express = require('express');
const router = express.Router();
const request = require('request')

// (GET) Find the number of articles for the query that matchs with the period
router.get('/', (req, res) => {
  if (typeof req.query.startDate =="undefined")
    {
      startDate = "1900/01/01";      
    }
  else{
    startDate = req.query.startDate;
  }
  if (typeof req.query.endDate =="undefined")
    {
      endDate = "3000/01/01";      
    }
  else{
    endDate = req.query.endDate;    
  }

  const queryPeriod = `${req.query.searchQuery} AND ("${startDate}"[Date - Publication] : "${endDate}"[Date - Publication])`
  const url = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${queryPeriod}&usehistory=y&api_key=5b1bbe2ef2a0bebe85a9937c9d71e9085f09;`;
  try{
   request(url, function (error, response, body) {
     //console.log('error:', error); // Print the error if one occurred
     //console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:', body); // Print the HTML for the Google homepage.
     const xml = body;
     parseString(xml, function (err, result) {
         //console.log(JSON.stringify(result));
         let retObj = new Object()
         retObj.pmidCount = result['eSearchResult']['Count']
         res.send(retObj);
     });
   });
  }
  catch(exception){
   res.send("Error, try send the GET request agian");
  }
  
});

module.exports = router;

