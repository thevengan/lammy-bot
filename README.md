# lammy-bot
SINoALICE All-in-One Discord Bot Built on Discord.py  
Developed and maintained by [@michael-arroyo](https://github.com/michael-arroyo) ([Vengan#7777](https://discordapp.com/users/235406385469194241))

![](/images/lammy.png)

## Features
- Easy setup in any server
- @ mentions for conquest, guerilla, and purification
- Weapon lookup
- Weapon Skill lookup
- Nightmare lookup
- Job lookup

## Coming Soon
- Conquest lookup

## Adding the Bot to Your Server
- Click on [this link here](https://discord.com/api/oauth2/authorize?client_id=824036912296886282&permissions=2415979536&scope=bot)

## Available Commands
### Prefix - use `!soa[command]` to access bot commands - eg. `!soahowto`
- `howto` : sends a DM to the message author detailing the commands available.
- `initialize` : creates the necessary channels and roles for `lammy-bot` to function.
    - what this entails - creates `sino_conquest`, `sino_guerrilla`, and `sino_purification` as server roles. Creates the `bot-spam` channel for using other commands.
- `giverole [role]` : gives the message author the requested role(s). Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
    - example - `!soagiverole conquest guerrilla` would give the message author the `sino_conquest` and `sino_guerrilla` roles.
- `removerole [role]` : removes the requested role(s) from the message author. Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
    - example - `!soaremoverole purification` would remove the `sino_purification` role from the message author.
- `toggle [@mention]` : toggles the requested @mention for the current server. Multiple @mentions can be given by separating them with a `space`. Possible @mentions are `conquest, guerrilla, purification`. You can turn off an @mention at the same time you turn another @mention off.
    - example - `!soatoggle guerrilla conquest` would toggle the @mentions for the `sino_guerrilla` and `sino_conquest` roles for the current server.
- `channel [channel_name]` : sets a custom channel for `lammy-bot` to listen for commands in. You can then delete any channels created by/for `lammy-bot`.
    - example - `!soachannel sino-bots` would look for the channel `sino-bots` in your server and, if it exists, set as a channel that you can use `lammy-bot` with.
- `weapon [weapon]`: searches the weapon database for the text entered after the command and returns an embed with information on the most relevant weapon.
    - example - `!soaweapon entrail` would pull up an embed with information for `Entrails of Justice`.
- `skill [skill]` : searches the skill database for the text entered after the command and returns an embed with information on the most relevant skill.
    - example - `!soaskill hero's harmony` would pull up an embed with information for `Hero's Harmony (I)`.
- `nightmare [nightmare]` : searches the nightmare database for the text entered after the command and returns an embed with information on the most relevant nightmare.
    - example `!soanightmare uga` would pull up an embed with information for `Ugallu`.
- `job [character]/[job]` : searches the class database for the text entered after the command and returns an embed with information on the most relevant class.
    - example `!soajob three little pigs/minstrel` would pull up an embed with information for `Three Little Pigs/Minstrel`.
    - **this command can take shortened character and class names as long as they are part of the whole name.**
        - **`!soajob red/lust` would work, but neither `!soajob rrh/lust` nor `!soajob red/l scorp` would work.**
- **(coming soon)** `conquest [conquest boss]` : searches the conquest database for the text entered after the command and returns an embed with strategy and information about the most relevant conquest boss.
    - example - `!soaconquest prom` would pull up the stategy embed for `Prometheus`

## Collaborators
- [@soaglobalguides](https://soaglobalguides.github.io/) ([danbodrop#0816](https://discordapp.com/users/138425084040839168))
    - Conquest boss guides
    