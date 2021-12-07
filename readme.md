# dnd session helper

A tool that helps DMs to relay vital information using discord. In dnd campaign, there is interactions and situations where there needs to be text and images sent.

## Important Concepts

### cli vs server

the cli is method that you use to create, change and remove content. the commands tables is below.

#### Screen

|command|arguments|notes|
|---|---|---|
|cat|`hex`| this allows you to view a screen by the hex |
|cp| `hex`| this copys a segment to your clip that can be pasted in the discord chat|
|ls|| this diplays a table showing all.|
|mk|`title`, `--pic`, `--soundtrack`, `--dm_notes`, `--pl_notes`|this creates a new screen|
|rm|`hex`| remove screen by hex|
|update|||
|-- notes|`hex`, `dm|pl`|this allows you update notes, by importing the hex then `dm` for the dm notes or `pl` for players notes|
|-- picture|`hex`,`url|path`|this will allow you to update the img that a hex uses|
|-- soundtrack|`hex`,`url|path`|this will allow you to update the img that a hex uses|
|-- title|`hex`, `new title`|this will allow you to update the title|

#### campaign

|command|arguments|notes|
|---|---|---|
|active|`id`|sets the active campign with in the system |
|ls||this prints a table of campaigns in the system |
|mk|`name`, `bio`|creates a new campaign|

#### combat

|command|arguments|notes|
|---|---|---|
|ls||table of combat|
|mk|`name`, `url`|creates a combat element|
|rm| `id`| removes combat by id|

___

### Screen Details

A Screen is a snapshot; this can be an NPC (non-playable character), giving the party a letter, a menu. The screen is made up of the following;

- hex; the hex is a four-digit code, which is made up letters and numbers and is used to fetch a screen.
- soundtrack; this soundtrack is a `Groovy` compatible URL this talked about later.
- picture; this can be an image path on your local system or a URL.
- title; this title is something that helps you remember what the content is.
- dm notes; these note that will appear on the server screen  
- pl notes; these note are sent to the discord server.
