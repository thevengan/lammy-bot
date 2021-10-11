# lammy-bot
SINoALICE All-in-One Discord Bot Built on Discord.py  
Developed by @michael-arroyo ([Vengan#7777](https://discordapp.com/users/235406385469194241)) and @soaglobalguides ([danbodrop#0816](https://discordapp.com/users/138425084040839168))

![](/images/lammy.png)

## Features
- Easy setup in any server
- @ mentions for conquest, guerilla, and purification
- Weapon lookup
- Weapon Skill lookup

## Coming Soon
- Nightmare lookup
- Conquest lookup

## Adding the Bot to Your Server
- Click on [this link here](https://discord.com/api/oauth2/authorize?client_id=824036912296886282&permissions=8&scope=bot)

## Available Commands
### Prefix - use `!soa[command]` to access bot commands - eg. `!soahelp`
- `help` : sends a DM to the message author detailing the commands available.
- `initialize` : creates the necessary channels and roles for `lammy-bot` to function.
    - what this entails - creates `sino_conquest`, `sino_guerrilla`, and `sino_purification` as server roles. Creates the `bot-spam` channel for using other commands.
- `giverole [role]` : gives the message author the requested role(s). Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
    - example - `!soagiverole conquest guerrilla` would give the message author the `sino_conquest` and `sino_guerrilla` roles.
- `removerole [role]` : removes the requested role(s) from the message author. Multiple roles can be given by separating them with a `space`. Possible roles are `conquest, guerrilla, purification`.
    - example - `!soaremoverole purification` would remove the `sino_purification` role from the message author.
- `weapon [weapon]`: searches the weapon database for the text entered after the command and returns an embed with information on the most relevant weapon.
    - example - `!soaweapon entrail` would pull up an embed with information for `Entrails of Justice`
- `skill [skill]` : searches the skill database for the text entered after the command and returns an embed with information on the most relevant skill.
    - example - 
- **(coming soon)** `nightmare [nightmare]` : searches the nightmare database for the text entered after the command and returns an embed with information on the most relevant nightmare.
    - example `!soanightmare uga` would pull up an embed with information for Ugallu.
- **(coming soon)** `conquest [conquest boss]` : searches the conquest database for the text entered after the command and returns an embed with strategy and information about the most relevant conquest boss.
    - example - `!soaconquest prom` would pull up the stategy embed for `Prometheus`