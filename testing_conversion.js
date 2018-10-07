var moment = require('moment');
var duration = 'PT15M51S';
var x = moment.duration(duration, moment.ISO_8601);
console.log(x.asSeconds()); // => 951