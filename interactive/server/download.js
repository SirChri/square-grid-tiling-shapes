import { Router } from 'express';
import config from './config';
import utils from './utils';

const router = Router();

router.post('/input', (req, res) => {
	var input = utils.generateInputFileContent(req.body);

    res.setHeader('Content-disposition', 'attachment; filename=input.lp');
    res.setHeader('Content-type', 'text/plain');
    res.charset = 'UTF-8';
    res.write(input);
    res.end();
});

export default router;