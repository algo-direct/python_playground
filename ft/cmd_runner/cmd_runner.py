# this should run vis root user
# read command from cmd_runner/todo/CmdUuid.cmd.json
# json file contains cmd_id, timeout adnd actual command
# write output to cmd_runner/output/

import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d pid:%(process)d; %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)25s() ] %(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
)
logging.info("Starting cmd_runner")

import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log = open("cmd_runner_sub_processes.log", "a")


class ExampleHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        try:
            if str(event.event_type) != "closed":  # check file close
                return
            if event.is_directory:  # exclude directries
                return
            logging.info(
                f"""Got
                        event_type: {event.event_type}
                        event_type: {type(event.event_type)}
                        is_directory: {event.is_directory}
                        is_directory: {type(event.is_directory)}
                        src_path: {event.src_path}
                        """
            )
            cmd_file = event.src_path[event.src_path.find("/") + 1 :]
            p = subprocess.Popen(
                [sys.executable, "cmd_runner_sub_proc.py", cmd_file],
                stdout=log,
                stderr=log,
            )
            logging.info(f"Started cmd_runner_sub_proc.py {cmd_file}, pid: {p.pid}")
        except:
            logging.exception("exception occured")
            logging.error(f"while processing event: {event}")


observer = Observer()
event_handler = ExampleHandler()  # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path="todo")
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
