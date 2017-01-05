/*
 * Local server API file. Packages needed for run: node, npm and then install with npm: 
 *  npm -install node-restful sqlite3 body-parser
 *
 */

// Dependencies
var express = require('express');
var app = express();
var fs = require('fs');
var cors = require('cors');

app.use(cors());
app.set('json spaces', 2);

// Sqlite3 database
var sqlite3 = require('sqlite3').verbose();
var dbPath = './Mountains.db';
var dbExists = fs.existsSync(dbPath);

// Checking if the database file is created, if not then the program will print an error message and exit.
if(!dbExists)
{
    console.log('Database not found in this folder, please use scrapemountain.py to get a mountain database.');
    process.exit();
}

var db = new sqlite3.Database(dbPath);
var bodyParser = require('body-parser');

///////////////////////////////////////////////////////////////////////////

var sql = "SELECT * FROM mountain;";

app.get('/mountains', function(req, res) {
    console.log("Request handler GET was called.");
    db.all(sql, function(err,rows) {
        // var rows2 = JSON.stringify(rows, null, 4);
        res.json(rows);
    });
});

// Setting up localserver.
app.listen(3000);


