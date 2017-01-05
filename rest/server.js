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
        res.end(JSON.stringify(rows));
    });
});



// get method to list up all mountains in json.
// Will get result from http://ip:3000/mountains
/*app.get('/mountains', function(req, res) {
    
    fs.readFile(__dirname + "/" + "mountains.json", 'utf8', function(err, data) {
        res.end(data);
    });
});*/

// Setting up localserver.
var server = app.listen(3000, function() {
    
    var host = server.address().address;
    var port = server.address().port;

    console.log("Example app listening at http://%s:%s", host, port);
});

