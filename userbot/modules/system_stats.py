# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot Module For Getting Information About The Server. """


import asyncio
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import __version__, version
import platform
import sys
import time
from datetime import datetime
import psutil
from userbot import (
    ALIVE_LOGO,
    ALIVE_NAME,
    BOT_VER,
    CMD_HELP,
    StartTime,
    UPSTREAM_REPO_BRANCH,
    INSTAGRAM_ALIVE,
    bot
)
from userbot.events import register


# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


modules = CMD_HELP


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]

    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "💻 **Informasi Sistem**\n"
    softw += f"`Sistem   : {uname.system}`\n"
    softw += f"`Rilis    : {uname.release}`\n"
    softw += f"`Versi    : {uname.version}`\n"
    softw += f"`Mesin    : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "📉 **Informasi CPU**\n"
    cpuu += "`Physical cores   : " + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "📉 **CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`Semua Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "📊 **Memori Digunakan**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "📁 **Bandwith Digunakan**\n"
    bw += f"`Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "⚙️ **Informasi Mesin**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if not event.text[0].isalpha() and event.text[0] not in (
            "/", "#", "@", "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await event.edit(
                "`Lynx Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`"
            )
        else:
            await event.edit(
                "Shame that you don't have git, you're running - 'v1.beta.4' anyway!"
            )


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Mencari...`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output Terlalu Besar, Dikirim Sebagai File`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await pip.edit("Gunakan `.help pip` Untuk Melihat Contoh")


@register(outgoing=True, pattern=r"^\.(?:lynx|xon)\s?(.)?")
async def amireallyalive(alive):
    logo = ALIVE_LOGO
    output = (
        f"`Robot` is running on `{repo.active_branch.name}`\n"
        "`====================================`\n"
        f"🐍 `Python         :` v{python_version()}\n"
        f"⚙️ `Telethon       :` v{version.__version__}\n"
        f"💻 `System         :` {uname.system}\n"
        f"👤 `User           :` {DEFAULTUSER}\n"
        "`====================================`\n"
        "📊 **Memory in use**\n"
        f"`Total     : {get_size(svmem.total)}`\n"
        f"`Available : {get_size(svmem.available)}`\n"
        f"`Used      : {get_size(svmem.used)}`\n"
        f"`Percentage: {svmem.percent}%`\n"
        "`====================================`\n"
    )
    if ALIVE_LOGO:
    try:
        logo = ALIVE_LOGO
        await bot.send_file(alive.chat_id, logo, caption=output)
        await alive.delete()
    except MediaEmptyError:
        await alive.edit(
            output + "\n\n *`The provided logo is invalid."
            "\nMake sure the link is directed to the logo picture`"
        )
else:
    await alive.edit(output)


@register(outgoing=True, pattern=r"^\.(?:kenzo|iam)\s?(.)?")
async def amireallyalive(alive):
    await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    output = (
        f"**ㅤㅤㅤㅤ ⚡【𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏】⚡**\n"
        f"╔══════════╣۩ ✞ ۩╠══════════╗ \n"
        f"╟⟩⟩ 🤴 • `ᴏᴡɴᴇʀ    :`[ＫΞＮＺＯ](t.me/SyndicateTwenty4)             ㅤ ║\n"
        f"╟⟩⟩ 🖥️ • `ꜱʏꜱᴛᴇᴍ.   :`Ubuntu 20.10            ║\n"
        f"╟⟩⟩ ⚙️ • `ᴛᴇʟᴇᴛʜᴏɴ  :`v.{version.__version__}                ㅤㅤ  ║\n"
        f"╟⟩⟩ 🐍 • `ᴘʏᴛʜᴏɴ.   :`v.{python_version()} ㅤㅤㅤㅤ         ║\n"
        f"╟⟩⟩ 👾 • `ʙᴏᴛ      :`v.{BOT_VER}                ㅤㅤㅤ ║\n"
        f"╟⟩⟩ 📂 • `ᴍᴏᴅᴜʟᴇ   :`{len(modules)} ㅤㅤㅤㅤㅤㅤㅤ   ║\n"
        f"╚══════════╣۩ ✞ ۩╠══════════╝ \n"
        f"🐈 : [𝗥𝗘𝗣𝗢-𝗟𝘆𝗻𝘅](https://kenzo-404.github.io/Lynx-Userbot)\n👥 : [𝗟𝘆𝗻𝘅-𝗧𝗲𝗮𝗺](t.me/GroupTidakDiketahui)")
    if ALIVE_LOGO:
    try:
        logo = ALIVE_LOGO
        await bot.send_file(alive.chat_id, logo, caption=output)
        await alive.delete()
    except MediaEmptyError:
        await alive.edit(
            output + "\n\n *`The provided logo is invalid."
            "\nMake sure the link is directed to the logo picture`"
        )
else:
    await alive.edit(output)


@register(outgoing=True, pattern=r"^\.(?:alive|on)\s?(.)?")
async def iamreallyalive(alive):
    user = await bot.get_me()
    await get_readable_time((time.time() - StartTime))
    await alive.edit("__Connecting to server.__")
    await alive.edit("__Connecting to server..__")
    await alive.edit("__Connecting to server...__")
    await alive.edit("__Connecting to server.__")
    await alive.edit("__Connecting to server..__")
    await alive.edit("__Connecting to server...__")
    await alive.edit("__Connecting to server.__")
    await alive.edit("__Connecting to server..__")
    await alive.edit("__Connecting to server...__")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡              🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡             🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡            🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡           🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡          🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡         🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡        🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡       🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡      🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡     🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡    🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡   🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡  🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡ 🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏🐈")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊🐈⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽🐈𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍🐈𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀🐈𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐𝙎🐈𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-𝙐🐈𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅-🐈𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻𝘅🐈𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆𝗻🐈-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟𝘆🐈𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡𝗟🐈𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡🐈𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("🐈𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡")
    await alive.edit("⚡")
    await asyncio.sleep(2.5)
    await alive.edit("😼")
    await asyncio.sleep(3)
    logo = ALIVE_LOGO
    output = (
        f"**ㅤㅤ  ╭─━━═━═━═━═━━─╮**\n"
        f"**       ⊏┊[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot) ⊨〛💨 **\n"
        f"**ㅤㅤ  ╰─━━═━═━═━═━━─╯**\n"
        f"╭╼════════════════════╾╮\n"
        f"│    ⇱  𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 𝐌𝐲 𝐏𝐫𝐨𝐟𝐢𝐥𝐞 ⇲ \n"
        f"┟╼════════════════════╾┤\n"
        f"╟◈ 👤  `Name     :` {DEFAULTUSER}\n"
        f"╟◈ 🔎  `Username :` @{user.username}\n"
        f"╟◈ ⚙️  `Telethon :` v. {version.__version__}\n"
        f"╟◈ 🐍  `Python   :` v. {python_version()}\n"
        f"╟◈ 👾  `Bot Ver  :` v. {BOT_VER}\n"
        f"╟◈ 🛠️  `Branch   :` {UPSTREAM_REPO_BRANCH}\n"
        f"╟◈ 💻  `System   :` {uname.system}\n"
        f"╟◈ 📂  `Plugins  :` {len(modules)}\n"
        f"┞╼════════════════════╾┤\n"
        f"├◈ **Don't forget to support our**\n"
        f"│    **userbot, how to press below.**\n"
        f"╰╼════════════════════╾╯\n"
        f"| [𝗥𝗲𝗽𝗼](https://kenzo-404.github.io/Lynx-Userbot) | [𝗟𝘆𝗻𝘅-𝗧𝗲𝗮𝗺](t.me/GroupTidakDiketahui) | "
        f"[𝗠𝘆 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺]({INSTAGRAM_ALIVE}) | ")
    if ALIVE_LOGO:
    try:
        logo = ALIVE_LOGO
        await bot.send_file(alive.chat_id, logo, caption=output)
        await alive.delete()
    except MediaEmptyError:
        await alive.edit(
            output + "\n\n *`The provided logo is invalid."
            "\nMake sure the link is directed to the logo picture`"
        )
else:
    await alive.edit(output)


@register(outgoing=True, pattern="^.edalive")
async def amireallyaliveuser(username):
    """For .aliveu command, change the username in the .alive command."""
    message = username.text
    output = ".aliveu [new username] tidak boleh kosong"
    if not (message == ".aliveu" and message[7:8] != " "):
        newuser = message[8:]
        global DEFAULTUSER  # global statement
        DEFAULTUSER = username
        output = "Successfully changed user to " + newuser + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    global DEFAULTUSER  # global statement
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully Reset User For Ur Alive!" "`")


CMD_HELP.update({
    "system": "✘ Pʟᴜɢɪɴ : System Stats"
    "\n\n⚡𝘾𝙈𝘿⚡: `.sysd`"
    "\n↳ : Shows system information using neofetch."
    "\n\n⚡𝘾𝙈𝘿⚡: `.db`"
    "\n↳ : Shows database related info."
    "\n\n⚡𝘾𝙈𝘿⚡: `.spc`"
    "\n↳ : Show system specification.",
    "alive": "✘ Pʟᴜɢɪɴ : Alive"
    "\n\n⚡𝘾𝙈𝘿⚡: `.lynx` or `.xon` or `.alive`"
    "\n↳ : To see whether your bot is working or not."
    "\n\n⚡𝘾𝙈𝘿⚡: `.edalive` <text>"
    "\n↳ : Changes the 'user' in alive to the text you want."
    "\n\n⚡𝘾𝙈𝘿⚡: `.restalive`"
    "\n↳ : Resets the user to default.",
    "botversion": "✘ Pʟᴜɢɪɴ : Robot Version"
    "\n\n⚡𝘾𝙈𝘿⚡: `.botver`"
    "\n↳ : Shows the userbot version."
    "\n\n⚡𝘾𝙈𝘿⚡: `.pip` <module(s)>"
    "\n↳ : Does a search of pip modules(s)."
})
