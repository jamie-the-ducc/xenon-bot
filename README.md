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

## Commands
`<arg>` = required

`[arg]` = optional

commands sepparated with a comma ( , ) do the same thing
### Prefix commands:

| Command            | Argument     | Function                                       |
|--------------------|--------------|------------------------------------------------|
| hello, reply | None         | replies to the sender                          |
| ping               | None         | replies with bot latency (ms)                  |
| avatar [arg]       | @user_tag    | sends profile picture of mentioned user        |
| rick, rickroll    | None         | sends rick roll gif 🙏                          |
| info               | None         | replies with bot name and the developers       |
| welcome \<arg>      | #channel_tag | sets the tagged channel to the welcome channel |


 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

Please make sure to update the tests as appropriate.
Thank you :)

## License

[MIT License](https://choosealicense.com/licenses/mit/)
