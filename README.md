# Awesome-PDF-for-students

Extract and translate text from SCANNED pdf. :zap:

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

  

