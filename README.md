Python 3 readiness
==================

Python 3 support graph for most popular Python libraries and packages http://py3readiness.org


## How do you identify Python 3 support?

This site utilizes little tool, [caniusepython3](https://github.com/brettcannon/caniusepython3) created by Brett Cannon. 

Throw your `requirements.txt` file at it and it will tell you which packages support Python 3, and list out which don't.

## Contribute

Please use issue tracker for issues, suggestions, feature requests and further enhancements.


## How does the site work?

The site works by checking PyPi periodically (currently daily).  
Script `generate.py` is run daily which generates JSON and updates date and time. 

For almost a year, the site was running on very low resource VPS with nginx as web server.  
Daily update was done via cron job in same machine.

Currently, `generate.py` function is run on AWS Lambda.   
It saves output JSON file to S3 which is used to build graph. Site itself is hosted on GitHub Pages.

## Local

Output (`results.json`, `wheel.svg`, `wheel.css`) are uploaded to S3. You need to configure `aws-cli`

1. `aws configure`
2. `python generate.py`

## Deploy

AWS Lambda needs all dependencies as zip file along with codebase. 

1.  `zip -r app.zip generate.py src/`
2. `cd path/to/site-packages/`
3. `zip -r app.zip *`

Finally, upload the app.zip file and update version.

## Credits

This is derivative work from [Python Wheels](https://pythonwheels.com), a site that tracks progress in new Python package distribution standard called [Wheels](https://pypi.org/project/wheel/). All the credits goes to [meshy](https://github.com/meshy).
