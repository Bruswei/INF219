var express = require('express');
var app = express();

var sqlite3 = require('sqlite3').verbose();
var db = './Mountains.db';

// Checking if the database file is created, if not then the program will print an error message and exit.
if(!dbExists)
{
    console.log('Database not found in this folder, please use scrapemountain.py to get a mountain database.');
    process.exit();
}
app.get('/', function(req, res){
  res.send('working');  
});

app.listen(3000);
console.log('API is running on port 3000!');


