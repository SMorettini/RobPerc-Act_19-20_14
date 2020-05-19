# Robotics Perception & Action Project 2019-20

## Group 14 - Safety Module

Team members:
- Boffo Marco
- Morettini Simone
- Rosales Pablo
- Rousseau Thomas

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

Could be usefull follow this link https://www.raffaelechiatto.com/modificare-permessi-di-esecuzione-di-script-in-powershell/

### Run Script

By running the script Measurement.py the module will collects data, analyses them and uses the
state machine to identify the different states.

```
python Measurement.py name_file seconds 
```
For example:
`
python Measurement.py test_run_1 10 
`
will save the data in a file named test_run_1 and it will run for 10 seconds

The script will print the actual state in the terminal. For use this module inside a mobile robots, the print of the state should be changed. Depending on the design of the system can be establish that some pins become high depending on the state of the module.

## Description of the repository content

* [Measurement.py](Measurement.py): it contains the main script of the module;
* [digital_acquisition.py](digital_acquisition.py): this file contains the code to read the signal converted by arduino and to convert it in a single value;
* [statemachine.py](statemachine.py): it contains the base class for implementing a state machine;
* [safetySM.py](safetySM.py): it contains the state machine with the states and the transition rules for our project;
* [utils.py](utils.py): collection of methods for data analysis and extraction of feature from the raw data.


The other files are used for tests or for minor function implementations.

## Important info

To leave this repository less heavy we put the data in another repository.
Rememeber to
```
git clone https://github.com/MesSem/RP-A_data.git
```
and to commit and push inside the folder RP-A_data for store new data and save on Github.

### Open and analyse the data DataAnalisys.ipynb (it's in RP-A_data.git)
```
pip install notebook
jupyter notebook
```
