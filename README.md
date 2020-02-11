# Robotics Perception & Action Project 2019-20

# NEW CLEANED REPOSITORY

## Group 14 - Safety Module

* Session 10/12 : Connected MEMS to RaspberryPi. Data acquisition functioning correctly.
	Future steps :
	* Work on current transducer
	* Setting up ADC with arduino
	* Current tests with LFG and oscilloscope
	* Implement threshold solution

* Session 11/12:
	* Added Threshold and data in the software
	* Prepared the Arduino

* Session 12/12 :  
	* Projected the dashboard
	* Prepare the current sensor


## Setup


### Linux

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

Create environment:
`py -m venv venv`

Activate environment:
`.\venv\Scripts\activate`
Install dependencies
`pip install -r ./requirements.txt`

### IMPORTANT INFO

Rememeber to

git clone https://github.com/MesSem/RP-A_data.git

and to commit and push inside the folder RP-A_data

### Run Script to collect Data

python Measurement.py name_file seconds (ex: python Measurement.py test_run_1 10)


https://www.raffaelechiatto.com/modificare-permessi-di-esecuzione-di-script-in-powershell/

#### To open and analyse the data DataAnalisys.ipynb
pip install notebook
jupyter notebook
