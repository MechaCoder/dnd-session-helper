# dnd session helper

A tool to asist Dungin masters who are useing discord.

in dnd a campain, Campain can be broken into sessions, and sessions can be broken down to seen, this tool, helps DM by outputing information that they need to players to see with a picture and text. this is bot that sits on the discoard server and the server.py is ran on your computer.

currently a sceen is made up of three concepts

+ title : a handy thing that will let you know what seen your looking at
+ picture: this can be a map, or a picture of an important chariter, something sets the seen for you and the players.
+ soundtrack: this is something that is played in the background, (this needs to be worked on)
+ notes: notes are split based on privete value (bool) if there are private then they will not be seen in discord but printed to the teminal window.

to have a working bot on your instance you need to have installed python3.7 and pipenv (google), and to set up the bot in your own [dev pannel](https://discord.com/developers/applications). you can run the server by runing pipenv run python server.py.

to interact with the data modual you will need to use, `cli.py`, the commands are based on simple unix commands (mk,ls and rm) and are grouped by the modeal, e.g. to create a sceen you would enter `pipenv run python cli.py screen mk 'this is a thing' --pic './test.jpg' --soundtrack 'youtubeVideo'`. use `pipenv run python cli.py --help` for more information

TODO:

+ work on makeing a sound player intergration
+ create an npc system
+ dice roll [1]
+ encoounter system

