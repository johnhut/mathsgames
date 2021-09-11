# Overview

The concept of this repo is to hold various simple maths games.

## Setup

Basic steps are:
- make sure you have python 3 installed (3.8 is what I used)
- clone repo
- create virtual environment (venv)
- install dependencies using setup.py
- check all is good with `black` and `flake8`
- run a game, e.g. `src/tuisnumberpairs.py`

You could do something like the following if running on linux/bash:

```
$ git clone git@github.com:johnhut/mathsgames.git
$ cd mathsgames
$ python3 -m venv .venv
$ . .venv/bin/activate
$ python -m pip install -U pip
$ pip install -e .
$ black src && flake8 src && python src/tuisnumberpairs.py
```

In powershell:
```
PS C:\> git clone git@github.com:johnhut/mathsgames.git
PS C:\> cd mathsgames
PS C:\> python -m venv .venv
PS C:\> .\.venv\Scripts\Activate.ps1
PS C:\> python -m pip install -U pip
PS C:\> pip install -e .
PS C:\> $(black .\src | Out-Host;$?) -and $(flake8 .\src\ | Out-Host;$?) -and $(python .\src\tuisnumberpairs.py)
```

## Game 1: Tui's Number Pairs

Goal is to stop numbers reaching the other side.  Recommended to start with a time between numbers
of 3000 ms.  1000 ms is a good speed.  500 ms is hard!

Change `NUM_ADD_INTERVAL` to select the ms between adding numbers to the screen.

### How to use

1. At any stage hit the escape key to exit the app.
2. Enter the number which will add to the left most digit to equal 10
3. Repeat step 2 quicker than the numbers pop up in the window
4. The game over screen and winning screens will show for a second before
   you can hit a key to restart.  This is just so you don't accidently miss
   end screen if you're madly hitting keys to avoid the end :-)
