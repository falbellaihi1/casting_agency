var connect = require('connect');
var serveStatic = require('serve-static');
appConnect = connect();


appConnect.use(serveStatic("platforms/browser/www"));

// CORS (Cross-Origin Resource Sharing) headers to support Cross-site HTTP requests
// src.all('*', function(req, res, next) {
//     res.header("Access-Control-Allow-Origin", "*");
//     res.header("Access-Control-Allow-Headers", "X-Requested-With");
//     next();
// });

// API Routes
// src.get('/blah', routeHandler);
appConnect.listen(process.env.PORT || 8000);
console.log('Please note that to test this, sometimes when you are already logged in to auth0, you need to clear cookies so that you are logged out');
// src.set('port', process.env.PORT || 5000);
//
// src.listen(src.get('port'), function () {
//     console.log('Express server listening on port ' + src.get('port'));
// });
