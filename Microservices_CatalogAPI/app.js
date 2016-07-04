require('newrelic');
var express = require('express');
var bodyParser = require('body-parser');
var cfenv = require("cfenv");
var path = require('path');
var cors = require('cors');

//Setup Cloudant Service.
var appEnv = cfenv.getAppEnv();
cloudantService = appEnv.getService("myMicroservicesCloudant");
var items = require('./routes/items');

var breakstuff = require('./routes/breakstuff')

//Setup ServiceDiscovery
var serviceDiscovery = require('./sd.js')

//Setup middleware.
var app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'www')));

//REST HTTP Methods
app.get('/db/:option', items.dbOptions);
app.get('/items', items.list);
app.get('/fib', items.fib);
app.get('/loadTest', items.loadTest);
app.get('/items/:id', items.find);
app.post('/items', items.create);
app.put('/items/:id', items.update);
app.delete('/items/:id', items.remove);

// Paths that will break stuff
app.get('/breakstuff/leakMemory', breakstuff.leakMemory);
app.get('/breakstuff/findUser/:username', breakstuff.findUser);
app.get('/breakstuff/badMethod', breakstuff.someBadMethod);
app.get('/breakstuff/findNemo', breakstuff.findNemo);


app.listen(appEnv.port, appEnv.bind);
console.log('App started on ' + appEnv.bind + ':' + appEnv.port);
