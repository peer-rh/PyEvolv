# PyEvolv v1.2 Beta

## What is PyEvolv
PyEvolv is an evolution simulator inspired by Evolvio by Karykh. As its name suggests it is implemented in python and pygame.

## Get Started
### First of all clone the repo and you're almost good to go.
```
git clone https://github.com/peerlator/PyEvolv.git
cd PyEvolv
```

### Then install the needed dependecies
```
pip install -r requirements.txt
pip install .
```

### Get Ready to start the game:
- Copy grids and constants.json to your home directory/.pyevolv/
```
cp examples/grids ~/.pyevolv/grids
cp examples/constants ~/.pyevolv/constants.json
```

### To Start a game:
``` 
pyevolv --constants_file default
```
To get more options:
```
pyevolv --help
```

## Tuning the hyper parameters
Edit the constants.json file in .pyevolv