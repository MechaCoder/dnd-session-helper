# dnd session helper

**In RPGs there is always a need to plan the campaign you (the DM) and the players with play though. this project is designed help with the.**

this tool is designed to work directly with discord and provide a way to provide the party with information, this is first done by manigming the information though a command line interface and then you can use the discord bot to

## How to use

becouse the project is mainly designed for `me` to use it best to use all the commands though useing pipenv, `pipenv run python cil.py` and useing `pipenv run python server.py`

### Commands

#### Actions

an action is a essentilly a path way for the party to follow, this will enable the DM to quickly though screen view to see where the party is going to next.

|command|attr|notes|
|---|---|---|
|mk|`too`, `from`| this command will create an action.
|rm|`hex`| this command will remove an action that is has a hex.

#### campaign

A campaign is a method of organizeing infomation so if your a dm like me you have a tendancy to work on many different campaigns at once

|command|attr|notes|
|---|---|---|
|active| campaignId |sets the active campaing only one campaign can be active at once|
|ls||list all campaigns|
|mk|`title`, `--bio` | this creates new campiagn.|

#### campaign player

this provide an easy way to add edit and remove players.

|command|attr|notes|
|---|---|---|
|ls||list all players in a compaign|
|mk|`name`| this will create a new player|
|rm|`doc_id`| removes by id the player|

#### Chat

this provide a method of reviewing a chat log.

|command|attr|notes|
|---|---|---|
|clear||this will delete all chat|
|read|| this will out put on as a table the chat log|

#### countdown

provides a method to create a terminal countdown that outputs, `--minutes` or `--hours`.

#### export

provides a method to export a campaign takes a campaign ID and

### gen

quickly allows people to generate NPC characters with complete profiles, takes `complex` or `simple`, simple will give you a quick profile and complex will give you a complete profile.

### screen

Screens are a colection of player notes, dm notes, soundtrack and a picture

|command|attr|notes|
|---|---|---|
|cat|`hex`|displays your a single screen|
|cp|`hex`|copys all data from one screen to new screen under a new hex|
|ls|| lists outs screens in a campaign|
|mk| `title` | creates a new screen|

### screen combat

an ecounter builder and reader.

### screen segment

repeatable sections that can be refenced and the content imported into scrren notes this is done by useing hex segment

### screen template

this provides a a dm a way to pre-define notes stucher in the settings.

## discord bot

`pipenv run python server.py` will run the bot from your computer, to use the bot you will need to set up a connection use the dev pannel, [link](https://discord.com/developers/applications)
