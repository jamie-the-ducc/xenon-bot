from configparser import ConfigParser
from datetime import datetime
from os import name, system
from os.path import isfile
from pathlib import Path

from colorama import Fore, Style

from app.__version__ import __version__

w = Style.BRIGHT + Fore.WHITE
BAD = f" {w}[{Fore.RED}x{w}]"
GOOD = f" {w}[{Fore.GREEN}+{w}]"
INFO = f" {w}[{Fore.BLUE}>{w}]"


reply_dict = {
    "rickroll":"https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713",
    "rick":"https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713",
    "info":"> I'm Xenon Bot! Coded by `[Jam!3]#4466`",
    "invite":"> Add me to your server!\n> https://discord.com/api/oauth2/authorize?client_id=943021878367359016&permissions=8&scope=bot"
}


reply_dict_noprefix = {
    "hi":"> Hi!",
    "hello": "> Hello!",
    "rick":"https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713",
    "rick roll":"https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713",
    "reply":"> I replied!",
    "mad":"😡",
    "happy":"😊",
    "sad":"😢",
    "love":"> I💜U",
    "flush":"<:flush_v2:946581195737665577>",
    "ducc":"<:ducc:946920331828920430>",
    "katt":"<:katt:946919968698667020>",
}


def clear() -> None:
    """Clears the terminal using the os.system function"""
    system("cls" if name in ("nt", "dos") else "clear")


def strip_codeblock(codeblock: str) -> str:
    if codeblock.startswith("```") and codeblock.endswith("```"):
        codeblock = codeblock.removeprefix('```')
        codeblock = codeblock.removesuffix('```')
        codeblock = codeblock.removeprefix('py')
        codeblock = codeblock.removeprefix('\n')
        codeblock = codeblock.removesuffix('\n')
    return codeblock


def title() -> None:
    """Prints the title of the program"""
    clear()
    b = Fore.LIGHTBLUE_EX
    c = Fore.LIGHTCYAN_EX
    title = fr"""{Style.BRIGHT}  {c}__{b}__  __   {c}__                                 
 | _{b}\ \/ /__{c}|_ |{b}_ __   ___  _ __    {c}_ __  _   _ 
 {c}| |{b} \  // _ \ {c}|{b} '_ \ / _ \| '_ \  {c}| '_ \| | | |
 {c}| |{b} /  \  __/ {c}|{b} | | | (_) | | | |{w}_{c}| |_) | |_| |
 {c}| |{b}/_/\_\___| {c}|{b}_| |_|\___/|_| |_{w}(_){c} .__/ \__, |
 {c}|__|{b}       {c}|__|{b}  {w}version {__version__}{c}   |_|    |___/{b}
 -----------------------------------------------{w}"""
    print(title)


def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def create_log():
    pass


def create_config() -> None:
    """Creates a bot configuration file (config.ini) with the requested parameters"""
    inpt = f" {w}[{Fore.YELLOW}-{w}]"
    file = "config.ini"
    config = ConfigParser()
    path = Path.cwd() / file

    prefix = input(f"{inpt} Bot prefix: ")
    token = input(f"{inpt} Bot token: ")
    webhook = input(f"{inpt} Webhook URL: ")
    owner = input(f"{inpt} Your Discord ID (owner): ")
    activities = input(f"{inpt} Bot statuses (separate multiple with comma): ")
    status_delay = input(f"{inpt} Bot status change delay: ")

    # Build config structure
    config.add_section("Xenon")
    config.set("Xenon", "s_prefix", prefix)
    config.set("Xenon", "s_token", token)
    config.set("Xenon", "s_webhook", webhook)
    config.set("Xenon", "i_owner", owner)
    config.set("Xenon", "s_activities", activities)
    config.set("Xenon", "f_status_delay", status_delay)

    with open(path, "w") as configfile:
        config.write(configfile)


def read_config(init = False):
    """Reads the bot configuration file (config.ini) and returns a config object"""
    if init:
        print(f'{INFO} Checking for "config.ini"...')
    file = Path.cwd() / "config.ini"
    config = ConfigParser()

    if isfile(file):
        config.read(file)
        if init:
            print(f'{GOOD} Loaded "config.ini" successfully')
        return convert_config(config["Xenon"].items())
    else:
        if init:
            print(f"{BAD} Failed to find config file. Please enter the following configuration information:")
        create_config()
        if init:
            print(f'{GOOD} Created "config.ini" successfully')
            print(f"{INFO} Make sure to re-run the program :)")
        title()
        read_config()


# source: https://stackoverflow.com/a/45417907
def convert_config(items):
    result = []
    for (key, value) in items:
        type_tag = key[:2]
        if type_tag == "s_":
            result.append((key[2:], value))
        elif type_tag == "f_":
            result.append((key[2:], float(value)))
        elif type_tag == "b_":
            result.append((key[2:], bool(value)))
        elif type_tag == "i_":
            result.append((key[2:], int(value)))
        else:
            raise ValueError(f'{BAD} Invalid type tag "{type_tag}" found in config.ini')
    return result


def display_bot_info(bot, prefix: str, activities: list):
    ready_time = get_time()
    title()
    
    length_a = (len(f"║ [+] Connected to Discord.com as {bot.user} ({bot.user.id})") - 1)
    length_b = len(f"║ [>] Status set to Listening to {activities[-1]}")
    length = length_a + 1 if length_a > length_b else length_b + 1

    header = " ╔" + " Bot Information ".center(length, "═") + "╗"
    connect_len = length - length_b
    status_len = length - length_a
    guild_len = length - len(f"║ [>] Watching {len(bot.guilds)} server(s) ⭐")
    prefix_len = length - len(f"║ [>] Prefix set to {prefix}")
    ready_len = length - len(f"║ [>] Bot ready at {ready_time}")

    bot_info = f"""{header}
 ║{GOOD} Connected to Discord.com as {Fore.GREEN}{bot.user}{w} ({Style.DIM}{bot.user.id}{Style.RESET_ALL}{w}){" " * status_len}║
 ║{INFO} Watching {Fore.YELLOW}{len(bot.guilds)} server(s){w} ⭐{" " * guild_len}║
 ║{INFO} Prefix set to {Fore.YELLOW}{prefix}{w}{" " * prefix_len} ║
 ║{INFO} Status set to {Fore.YELLOW}Listening to {activities[-1]}{w}{" " * connect_len} ║
 ║{INFO} Bot ready at {Fore.YELLOW}{ready_time}{w}{" " * ready_len} ║
 ╚{"═" * length}╝"""
 
    return  bot_info
