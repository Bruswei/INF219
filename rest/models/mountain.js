
// Dependency
var restful = require('node-restful');

// Sqlite3 database
var sqlite3 = require('sqlite3').verbose();
var db = '../Mountains.db';

// Schema
var mountainSchema = new sqlite3.Schema({
    name: String,
    id: Number,
    height: Number,
    pf: Number,  
});

// Return model
module.exports = restful.model('mountains', mountainSchema);
