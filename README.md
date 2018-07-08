<div align="middle">
<img src="https://github.com/DdukTwiSun/server/blob/master/logo.jpg" height="250px" >
</div>

<h1 align="center">Awesome-PDF-for-students</h1>

<p align="center">
	<a href="https://sigoss.github.io/hackathon2018/"><img src="https://img.shields.io/badge/OpenHack-3th-blue.svg"></a>
	<a href="https://github.com/DdukTwiSun/server/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>	
</p>

Extract and translate text from SCANNED pdf. :zap:

## Overview

<img src="https://github.com/DdukTwiSun/server/blob/master/home_capture.PNG?raw=true" style="width:888;"/>

![INTRO](https://github.com/DdukTwiSun/server/blob/master/intro.jpg)


*****

1. [Demo](#demo)
2. [Installation](#installation)
3. [License](#license)
*****



## Demo

run http://openhack.make.codes/test



## Installation

Before installation,

this app uses The Google Cloud [VISION API](https://cloud.google.com/vision/) and [TRANSLATION API](https://cloud.google.com/translate), so you should take the following steps.
 
 Take steps 1 and 2 in the "before you begin" section :point_right: [here](https://cloud.google.com/translate/docs/quickstart).
  

:warning: **Since the Google API is a paid service, you may incur costs.**



The following procedure is based on ubuntu linux, and may differ depending on your operating system.

```bash

# git clone server repository.
> git clone https://github.com/DdukTwiSun/server

# install python3 & venv.
> sudo apt-get install python3 python3-venv

# set up a virtual environment.
> python3 -m venv myvenv
> source myvenv/bin/activate

# install all requirement packages.
> pip install -r requirements.txt

# upgrade the client library.
pip install --upgrade google-cloud-vision

# 1) run server on your local system.
> flask run
# If the flask is running successful, try connecting to http://127.0.0.1:5000/test and doing test.


# 2) run server on cloud server at port 80.
> sudo FLASK_APP=server/api.py myvenv/bin/python3 -m flask run --host=0.0.0.0 --port=80
# If the flask is running successful, try connecting to http://yourserver:80/test and doing test.

```

If your server is ready, start the client.
You need to install node.js & npm.

```bash

# git clone Client repository.
> git clone https://github.com/DdukTwiSun/Client

 # install dependency for client.
 > npm install

 # Modify the code for your server.
 # base.js   line 33) const translateApiUrl = http://yourserver/translate/
 # home.html line 11) data-url="http://yourserver/upload"/>

# start your client and run your example.
> npm start 

# try connecting to http://yourserver:8080/home.html and upload your PDF.
```

## License

* [MIT License](LICENSE)

  

