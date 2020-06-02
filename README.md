### gold-main

gold-main is simple python tool for programmatically beating top offers on cardsphere.com

gold-main gets a sorted list of top offers from cardsphere's Rest API and uses that, in combination with a wants export of yours, to beat the top offer on each card in your wants export by $0.02 (the smallest price difference guaranteed to cause the seller to recieve additional funds). 

### Help Support gold-main and other Magic trading tools

Paypal link go here

### Installation

#### Prerequisites

1. Python (2 or 3 should work)
1. Git (optional)
1. Pip (usually comes with Python)

#### Mac / Linux

1. Clone this repository with `git clone https://github.com/markus-leben/Gold.main.git`
or download the [latest release](https://github.com/tomreece/markus-leben/Gold.main/master.zip)
1. Open Terminal.
1. Go to the Pucauto folder you just cloned or downloaded with `cd /path/to/pucauto`
1. Run `sudo pip install -r requirements.txt` and enter your system password
when prompted.

#### Windows

1. Clone this repository with `git clone https://github.com/tomreece/pucauto.git`
or download the [latest release](https://github.com/tomreece/markus-leben/Gold.main/master.zip).
1. Download Python from https://www.python.org/downloads/
1. Install Python **IMPORTANT:** Select the check box to **Add python.exe to Path**.
1. Unzip and open the Gold.main folder.
1. Shift + Right-Click, then select "Open command window here".
1. Run the command `python -m pip install -r requirements.txt`

### Configuring

1. Open `config.json` in a plain text editor like Notepad or Sublime
Text.
1. Enter your Cardsphere username and password in place of the default values in
the file. Be sure to keep the quotes around the values.
1. Add any usernames, user_id's, country names, or country initials to their respective whitelists and blacklists. It's usually a good idea to ad yourself to the user blacklist, unless you want to be beating your own price if you're the current top offer. 
1. Save the file as `config.json`.
1. Drag and drop a cardsphere wants export file into the folder that contains gold-main.py
1. You'll get an error on startup if you have no `config.json`, no cardsphere_wants_\[datetime\].csv, or you have no username and password in there. 


### Running

At this point you should be able to run gold-main with:

`run gold-main.py`

or by double clicking gold-main.py, or by running it in your IDE of choice. When cold caching it will take quite a while for the program to load offers. This is normal. After it's done running it will spit out a file named `output.csv`. This file should be a ready-to-import wants file that beats all other users wants for cards in your original .csv file. 
