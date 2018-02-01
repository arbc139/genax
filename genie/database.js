const mysql = require('mysql2/promise');
const config = require('config');

const argv = require('./argv');

const dbConfig = config.get('genie.dbConfig');

function getField(config, field) {
  return config.get(field) ? config.get(field).toString() : '';
}

// Creates pool to MySQL database.
const pool = mysql.createPool({
  connectionLimit: 10,
  database: getField(dbConfig, 'database'),
  host: getField(dbConfig, 'host'),
  user: argv.user,
  password: argv.password,
});

// Uses query like this.
/**
 * database.query(
 *     `SELECT * FROM 'table' WHERE 'name' = ${name} AND 'age' > ${age}`)
 *     .then(rows => {});
 *
 * rows: Contains rows returned by server
 */
module.exports = {
  query: async function(query) {
    const connection = await pool.getConnection();
    const [rows] = await connection.execute(query);
    await connection.release();
    return rows;
  },
};
