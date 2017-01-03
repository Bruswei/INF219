/*
 * Local server API file. Packages needed for run: node, npm and then install with npm: 
 *  npm -install node-restful sqlite3 body-parser
 *
 */

// Dependencies
var express = require('express');
var app = express();
var fs = require('fs');

// Sqlite3 database
var sqlite3 = require('sqlite3').verbose();
var db = './Mountains.db';
var dbExists = fs.existsSync(db);

var bodyParser = require('body-parser');

// Checking if the database file is created, if not then the program will print an error message and exit.
if(!dbExists)
{
    console.log('Database not found in this folder, please use scrapemountain.py to get a mountain database.');
    process.exit();
}

/********************************************************************/

// Express
var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//app.get('/', function(req, res){
//  res.send('working');  
//});
//

// Routes
app.use('/api', require('./routes/api'));

// Start server
app.listen(3000);
console.log('API is running on port 3000!');



