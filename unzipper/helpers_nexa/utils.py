# ===================================================================== #
#                      Copyright (c) 2022 Itz-fork                      #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  #
# See the GNU General Public License for more details.                  #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>   #
# ===================================================================== #
# Credits: SpEcHiDe's AnyDL-Bot

from re import sub
from os import path, walk
from time import time
from math import floor
from functools import partial
from subprocess import Popen, PIPE
from asyncio import get_running_loop


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n**Process**: {2}%\n".format(
            ''.join(["█" for i in range(floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\n**Speed:** {2}/s\n**ETA:** {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(text="{}\n {} \n\n**Powered by @NexaBotsUpdates**".format(ud_type, tmp))
        except:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


def run_shell_cmds(command):
    """
    Execute shell commands and returns the output
    """
    run = Popen(command, stdout=PIPE,
                stderr=PIPE, shell=True)
    shell_ouput = run.stdout.read()[:-1].decode("utf-8")
    return shell_ouput


async def run_cmds_on_cr(func, *args, **kwargs):
    """
    Execute blocking functions asynchronously
    """
    loop = get_running_loop()
    return await loop.run_in_executor(
        None,
        partial(func, *args, **kwargs)
    )


async def get_files(fpath: str):
    """
    Returns files in a folder

    Parameters:

        - `fpath` - Path to the folder
    """
    path_list = [val for sublist in [
        [path.join(i[0], j) for j in i[2]] for i in walk(fpath)] for val in sublist]
    return sorted(path_list)


async def rm_mark_chars(text: str):
    """
    Remove basic markdown characters

    Parameters:

        - `text` - Text
    """
    return sub("[*`_]", "", text)