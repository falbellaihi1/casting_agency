var express = require('express');
var app = express()
app.use(express.static('www'));
app.set('port', process.env.PORT || 5000);
app.listen(app.get('port'), function () {
    console.log('port', app.get('port'));
});


