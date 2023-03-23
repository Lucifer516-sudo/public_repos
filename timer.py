import datetime

import logging

import sys

import os

import subprocess

import time

from rich.console import Console

from rich.progress import Progress, BarColumn, TimeRemainingColumn

import typer

import signal

app = typer.Typer()

console = Console()

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(handler)

time_remain_str = ""

def run_timer(minutes: int, progress_bar: bool, format: str):

    seconds = minutes * 60

    start_time = datetime.datetime.now()

    end_time = start_time + datetime.timedelta(seconds=seconds)

    if progress_bar:

        with Progress("[progress.description]{task.description}", BarColumn(), "[progress.percentage]{task.percentage:>3.0f}%", TimeRemainingColumn()) as progress:

            task = progress.add_task("Timer", total=seconds)

            while datetime.datetime.now() < end_time:

                progress.update(task, advance=1)

                try:

                    # Sleep for 1 second before checking the time again

                    datetime.datetime.now().strftime("%S")

                except KeyboardInterrupt:

                    logger.info("Timer stopped by user")

                    sys.exit()

        console.print("Timer complete!")

        logger.info("Timer complete!")

    else:

        while datetime.datetime.now() < end_time:

            #            notification_id = 101010

            global time_remain_str

            terminal_size = os.get_terminal_size()

            remaining_time = int((end_time - datetime.datetime.now()).total_seconds())

            if format == 'hms':

                remaining_time_str = datetime.timedelta(seconds=remaining_time)

            elif format == 'ms':

                remaining_time_str = "{:02d} mins & {:02d} sec".format(*divmod(remaining_time, 60))

            else:

                remaining_time_str = f"{remaining_time} seconds"

            console.print(f"Time Remaining: {remaining_time_str}", end="\r")

            time_remain_str= remaining_time_str

            time_to_complete = f"{remaining_time/60}m Running"

            i = 1

            if i == 60:

                subprocess.run(['termux-notification',

                        '-t', 'Timer',

                            '-c', time_to_complete,

                                '--sound'])

            i += 1

            try:

                # Sleep for 1 second before checking the time again

                if terminal_size != os.get_terminal_size():

                    terminal_size = os.get_terminal_size()

                    console.clear()

                datetime.datetime.now().strftime("%S")

            except KeyboardInterrupt:

                logger.info("Timer stopped by user")

                sys.exit()

        message= f'Minutes: {minutes} completed !!!'

        subprocess.run(['termux-notification',

                '-t', 'Timer',

                        '-c', message,

                        '--sound'])

        console.print("Timer complete!")

        logger.info("Timer complete!")

@app.command()

def timer(minutes: int, progress_bar: bool = False, format: str = "default"):

    """Start a timer for the specified number of minutes."""

    with console.screen():

        console.clear()

        if format not in ['default', 'hms', 'ms']:

            logger.warning("Invalid format argument, using default")

            format = "default"

        run_timer(minutes, progress_bar, format)

def on_exit():

    typer.clear()

    message = f"Timer aborted with time left: {time_remain_str} !!!?"

    subprocess.run(['termux-notification',

                        '-t', 'Timer',

                        '-c', message,

                        '--sound'])

    sys.exit()

def interrupt_handler(signal, frame):

    on_exit()

    raise KeyboardInterrupt

signal.signal(signal.SIGINT, interrupt_handler)

if __name__ == "__main__":

        app()
