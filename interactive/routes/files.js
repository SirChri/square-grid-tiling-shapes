var config = require('./config');
var utils = require('./utils');

var express = require('express');
var router = express.Router();

router.post('/input', (req, res) => {
	var input = utils.generateInputFileContent(req.body);

    res.setHeader('Content-disposition', 'attachment; filename=input.lp');
    res.setHeader('Content-type', 'text/plain');
    res.charset = 'UTF-8';
    res.write(input);
    res.end();
});

module.exports = router;
