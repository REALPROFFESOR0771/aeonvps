import sys
from os import path, environ
from logging import (
    INFO,
    ERROR,
    Formatter,
    FileHandler,
    StreamHandler,
    info,
    error,
    getLogger,
    basicConfig,
)
from subprocess import run
from requests import get
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from requests import get

getLogger("pymongo").setLevel(ERROR)
getLogger("httpx").setLevel(ERROR)

if path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)


class CustomFormatter(Formatter):
    def format(self, record):
        return super().format(record).replace(record.levelname, record.levelname[:1])


formatter = CustomFormatter(
    "[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%d-%b-%y %I:%M:%S %p"
)

file_handler = FileHandler("log.txt")
file_handler.setFormatter(formatter)

stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

basicConfig(handlers=[file_handler, stream_handler], level=INFO)

load_dotenv('config.env', override=True)

try:
    if bool(environ.get('_____REMOVE_THIS_LINE_____')):
        log_error('The README.md file there to be read! Exiting now!')
        exit()
except:
    pass
    
BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    error("BOT_TOKEN variable is missing! Exiting now")
    sys.exit(1)

bot_id = BOT_TOKEN.split(":", 1)[0]

DATABASE_URL = environ.get("DATABASE_URL", "")
if len(DATABASE_URL) == 0:
    DATABASE_URL = None

if DATABASE_URL:
    conn = MongoClient(DATABASE_URL)
    db = conn.luna
    if config_dict := db.settings.config.find_one({"_id": bot_id}):
        environ["UPSTREAM_REPO"] = config_dict["UPSTREAM_REPO"]
        environ["UPSTREAM_BRANCH"] = config_dict["UPSTREAM_BRANCH"]
    conn.close()

UPSTREAM_REPO = environ.get("UPSTREAM_REPO", "")
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = 'https://github.com/REALPROFFESOR0771/AeonVps'

UPSTREAM_BRANCH = environ.get("UPSTREAM_BRANCH", "")
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = "main"

if path.exists(".git"):
    run(["rm", "-rf", ".git"], check=False)

update = run(
    [
        f"git init -q \
                 && git config --global user.email falgunpatel.fv@gmail.com \
                 && git config --global user.name lordgaruda \
                 && git add . \
                 && git commit -sm update -q \
                 && git remote add origin {UPSTREAM_REPO} \
                 && git fetch origin -q \
                 && git reset --hard origin/{UPSTREAM_BRANCH} -q"
    ],
    shell=True,
    check=False,
)

if update.returncode == 0:
    info("Successfully updated with latest commit from UPSTREAM_REPO")
else:
    error(
        "Something went wrong while updating, check UPSTREAM_REPO if valid or not!"
    )
