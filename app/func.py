from configparser import ConfigParser
from datetime import datetime
from os import name, system
from os.path import isfile
from pathlib import Path

from colorama import Fore, Style

from app.__version__ import __version__


w = Style.BRIGHT + Fore.WHITE
BAD = f" {w}[{Fore.RED}x{w}]"


def clear() -> None:
    """Clears the terminal using the os.system function"""
    system("cls" if name in ("nt", "dos") else "clear")


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
 {c}|__|{b}       {c}|__|{b}    {w}version {__version__}{c}    |_|    |___/{b}
 -----------------------------------------------{w}"""
    print(title)


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
    status_delay = input(f"{inpt} Bot status change delay: ")

    # Build config structure
    config.add_section("Xenon")
    config.set("Xenon", "s_prefix", prefix)
    config.set("Xenon", "s_token", token)
    config.set("Xenon", "s_webhook", webhook)
    config.set("Xenon", "i_owner", owner)
    config.set("Xenon", "f_status_delay", status_delay)

    with open(path, "w") as configfile:
        config.write(configfile)


def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def create_log():
    pass


def read_config():
    good = f" {w}[{Fore.GREEN}+{w}]"
    bad = f" {w}[{Fore.RED}x{w}]"
    info = f" {w}[{Fore.BLUE}>{w}]"
    """Reads the bot configuration file (config.ini) and returns a config object"""
    print(f'{info} Checking for "config.ini"...')
    file = Path.cwd() / "config.ini"
    config = ConfigParser()

    if isfile(file):
        config.read(file)
        print(f'{good} Loaded "config.ini" successfully')
        return convert_config(config["Xenon"].items())
    else:
        print(
            f"{bad} Failed to find config file. Please enter the following configuration information:"
        )
        create_config()
        print(f'{good} Created "config.ini" successfully')
        print(f"{info} Make sure to re-run the program :)")
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
