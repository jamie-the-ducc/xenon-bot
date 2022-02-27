# [Xe]non Bot

[Xe]non is a Discord bot written in Python for general server use and moderation. 

(*COMPLETELY WIP AT THE MOMENT*)

![Xenon Bot](/app/img/preview.png?raw=true)

## Installation

Make sure you have `discord.py` uninstalled.
```bash
python -m pip uninstall -y discord.py
```
Clone the repository from GitHub. Then install all the dependencies.

```bash
git clone https://github.com/EnbyCosmog/xenon-bot
cd xenon-bot
python -m pip install -r requirements.txt
```

## Usage

Open `run.bat` to run the script.

```bash
Command prompt  ::  run.bat
Powershell      ::  .\run.bat
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

| Type     | Command                          | Argument         | Function                                           |
|----------|----------------------------------|------------------|----------------------------------------------------|
| bot      | l, ping, latency                 | none             | replies with bot latency (ms)                      |
| general  | hello, greet                     | none             | replies to the sender                              |
| general  | info                             | none             | replies with bot and developers names              |
| general  | rick, rickroll                   | none             | sends rick roll gif                                |
| general  | p, pfp, profile, avatar `<arg>`  | @user_tag        | sends profile picture of mentioned user            |
| general  | o, old, age, howold `<arg>`      | @user_tag        | returns account age + creation date                |
| general  | base64encode, b64e `[arg]`       | string           | returns string encoded in base64                   |
| general  | base64decode, b64d `[arg]`       | string           | returns decoded string from base64                 |
| admin    | w, welcome, setwelcome `<arg>`   | #channel_tag     | sets the tagged channel to the welcome channel     |
| admin    | kick `[arg]` `<arg>`             | @user_tag, reason| kicks mentioned member from the server             |
| admin    | ban `[arg]` `<arg>`              | @user_tag, reason| bans mentioned member from the server              |
| admin    | unban `[arg]`                    | @user_tag        | unbans mentioned banned member                     |
| admin    | timeout, to, tmout `[arg]` `[arg]` `<arg>` | @user_tag, time (minutes), reason| timeouts mentioned member for x amount of time |
| owner    | sd, shutdown, exit               | none             | owner only - turns off the bot (`client.close()`)  |
| owner    | e, eval `[arg]`                  | codeblock        | evaluates python code and returns results          |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

Please make sure to update the tests as appropriate.
Thank you :)

## License

[MIT License](https://choosealicense.com/licenses/mit/)
