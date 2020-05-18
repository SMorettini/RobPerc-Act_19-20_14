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
python Measurement.py name_file seconds (ex: python Measurement.py test_run_1 10)
```

The script will print the actual state in the terminal. For use this module inside a mobile robots, the print of the state should be changed. Depending on the design of the system can be establish that some pins become high depending on the state of the module.

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
