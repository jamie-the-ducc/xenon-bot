# [Xe]non Bot

[Xe]non is a Discord bot written in Python for general server use and moderation. 

(*COMPLETELY WIP AT THE MOMENT*)

![Xenon Bot](/app/img/preview.png?raw=true)

## Installation

Clone the repository from GitHub. Then install all the dependencies.

```bash
git clone https://github.com/EnbyCosmog/xenon-bot
cd xenon-bot
pip install -r requirements.txt
```
Make sure you have `discord.py` uninstalled first:
```bash
pip uninstall -y discord.py
```

## Usage

Open `run.bat` to run the script.

```bash
run.bat
```
If you're running the script for the first time, you'll need to fill out some information for the `config.ini` file. It stores important variables such as your bot token and prefix.

## Bot Features
### Functionality:
- Welcomes/says goodbye to members as they join/leave the server
  - need set welcome channel first (`welcome <#channel_tag>`) 
- Responds to commands (see below)

### Prefix commands:

| `[arg]` = required | `<arg>` = optional |
|--------------------|--------------|

| Command            | Argument     | Function                                       |
|--------------------|--------------|------------------------------------------------|
| hello, reply       | None         | replies to the sender                          |
| info               | None         | replies with bot and developers names          |
| ping               | None         | replies with bot latency (ms)                  |
| welcome \[arg]     | #channel_tag | sets the tagged channel to the welcome channel |
| avatar <arg>       | @user_tag    | sends profile picture of mentioned user        |
| rick, rickroll     | None         | sends rick roll gif                            |
| shutdown           | None         | owner only, turns off the bot(`client.close()`)|
| eval [arg]       | Python codeblock| evaluates python codeblock and returns results|
 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

Please make sure to update the tests as appropriate.
Thank you :)

## License

[MIT License](https://choosealicense.com/licenses/mit/)
