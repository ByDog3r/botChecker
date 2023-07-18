from time import sleep
from pickle import load
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio, logging, sys
from src.tools.doxxer import dox
from src.tools.delck import delckc
from huepy import lightred, lightgreen
from src.tools.me import getMe as info_me
from src.tools.bin import bin as bin_info
from src.tools.gen import GeneatedCC as gen
from src.tools.cmds import CommandsFunction as cmd
from src.tools.me import StartFnction as start
from src.tools.cmds import cmd_buttons
from src.tools.gen import gen_buttons
from src.gates.stripe_mora import getLive
from src.tools.address import genAddress as faker
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, PrefixHandler, CallbackContext, CallbackQueryHandler


def banner():
    print(lightred("""
     /$$                           /$$                           /$$      
    | $$                          | $$                          | $$      
    | $$$$$$$  /$$   /$$  /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$
    | $$__  $$| $$  | $$ /$$_____/| $$__  $$ /$$__  $$ /$$_____/| $$  /$$/
    | $$  \ $$| $$  | $$| $$      | $$  \ $$| $$$$$$$$| $$      | $$$$$$/ 
    | $$  | $$| $$  | $$| $$      | $$  | $$| $$_____/| $$      | $$_  $$ 
 /$$| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
|__/|_______/  \____  $$ \_______/|__/  |__/ \_______/ \_______/|__/  \__/
               /$$  | $$                                                  
              |  $$$$$$/                                                  
               \______/                                                   \n"""))

with open("src/assets/.token", 'rb') as T:
    TOKEN = load(T)

#========= start Command ===========
async def start_command(update: Update, _) -> None:
    await start(update, ParseMode.HTML)

# ======== CMDS FUNCTIONS ==========
async def cmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE, key = InlineKeyboardButton , markup= InlineKeyboardMarkup) -> None:
    await cmd(update, context, key, markup, ParseMode.HTML)

async def cmd_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, key = InlineKeyboardButton , markup= InlineKeyboardMarkup):
    await cmd_buttons(update, context, key, markup, ParseMode.HTML)

# ======== Me function =============
async def me_command(update: Update, _) -> None:
    await info_me(update, ParseMode.HTML)

# ========== Fake address US =========
async def fakeaddress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await faker(update, context, ParseMode.HTML, ChatAction.TYPING)

# ======== BIN LOCKUP =============
async def binlookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bin_info(update, context, ParseMode.HTML, ChatAction.TYPING)

# =========== BIN GEN ================
async def gen_command(update: Update, context: ContextTypes.DEFAULT_TYPE, key = InlineKeyboardButton , markup= InlineKeyboardMarkup):
    await gen(update, context, key, markup, ParseMode.HTML, ChatAction.TYPING)

async def gen_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, key = InlineKeyboardButton , markup= InlineKeyboardMarkup):
    await gen_buttons(update, context, key, markup, ParseMode.HTML)
    
# ======== Dox Function ===============
async def dox_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dox(update, context, ParseMode.HTML, ChatAction.TYPING)

# ======== Remove Cache ===============
async def comando_delck(update: Update, _):
    await delckc(update, ParseMode.HTML)

# ======== STRIPE GATES ===============
async def stripe_gate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await getLive(update, context, ParseMode.HTML, ChatAction.TYPING)

logging.basicConfig(
    level=logging.ERROR
)

if __name__ == '__main__':

    banner()
    for i in (lightgreen("\t\t.bychecker is initied\n\n")):
        sys.stdout.write(i)
        sys.stdout.flush()
        sleep(1./12)

    #======= Start Bot ======
    application = ApplicationBuilder().token(TOKEN).build()

    #Command Handlers
    application.add_handler(PrefixHandler(['>', ">>"], ['>>', '>'], dox_command))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['me', 'Me', 'mi'], me_command))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['gen', 'Gen', 'GEN'], gen_command))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['bin', 'Bin', 'BIN'], binlookup_command))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['start', 'Start', 'START'], start_command)) 
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['faker', 'rand', 'address'], fakeaddress_command))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['cmds', 'cmd', 'commands'], cmd_command))
    application.add_handler(PrefixHandler(["/", "#", ".", ",", "!"], ["delck"], comando_delck))
    application.add_handler(PrefixHandler(['/', "#", '.', ',', "!"], ['mr'], stripe_gate_command))

    #KeyBoard Handlers
    application.add_handler(CallbackQueryHandler(cmd_keyboard))
    application.add_handler(CallbackQueryHandler(gen_keyboard))

    application.run_polling()
