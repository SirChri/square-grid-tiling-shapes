import { Router } from 'express';
import config from './config';
import utils from './utils';

var Clingo = require('clingojs');

const router = Router();

router.post('/', async (req, res) => {
	//set the appropriate HTTP header
	res.setHeader('Content-Type', 'application/json');

	//console.log(req.body)
	var clingo = new Clingo({
		clingo: config.clingo_path
	});
	
	var input = utils.generateInputFileContent(req.body);
	
	var out = {};
	await new Promise(resolve => clingo.solve({
		input: input,
		inputFiles: [config.main_file_path],
		maxModels: 0,
		args: [
			"--time-limit=300",
			"-t4",
			"--quiet=1,1",
			"--out-hide-aux",
			"--opt-strategy=bb,inc"
		]
	})
		.on('model', function (model) {
			if (model) {
				out["opt"] = false;
				if (model[0] == "OPTIMUM" && model[1] == "FOUND") {
					out["opt"] = true
				} else if (model[0] != "Optimization:") {
					var cells = model.map(function (r) {
						var vals = r.split("(")[1].split(")")[0].split(",");
						return {
							"val": vals[2],
							"x": vals[0],
							"y": vals[1]
						}
					});

					out["cost"] = cells.filter(r => r.val == "eee").length
					out["model"] = cells;

					//res.write(JSON.stringify(out))
				}
			}
		})
		.on('end', function () {
			res.write(JSON.stringify(out))
			// This function gets called after all models have been received
			resolve()
		}));

	//end the response process
	res.end();
});

export default router;