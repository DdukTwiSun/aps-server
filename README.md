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
  

:warning: **Since the Google API is a paid service, you may incur costs**



```bash
# set up a virtual environment
> python3 -m venv myvenv
> source myvenv/bin/activate

# install all requirement packages
> pip3 install -r requirements.txt

# run server
> flask run
```

## License

* [MIT License](LICENSE)

  

