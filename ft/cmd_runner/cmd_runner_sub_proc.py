import logging
import sys
import json
import subprocess

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d pid:%(process)d; %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)25s() ] %(message)s",
    datefmt="%Y-%m-%d_%H:%M:%S",
)
logging.info(f"Starting cmd_runner_sub_proc: {sys.argv}")


if len(sys.argv) < 2:
    logging.error("Please provide cmd file")

cmd_file = sys.argv[1]
cmd = json.load(open(f"todo/{cmd_file}"))
subprocess.run(["mv", f"todo/{cmd_file}", f"output/{cmd_file}"])
# json CmdUuid.cmd.json
logging.info(f"Running cmd: {cmd}")
cmd_id = cmd["cmd_id"]
timeout = int(cmd["timeout"])
bash_file_name = f"output/{cmd_id}.sh"
bash_file = open(bash_file_name, "w")
bash_file.write(cmd["command"])
bash_file.close()

stderr_file = open(f"output/{cmd_id}_stderr.txt", "w")
stdout_file = open(f"output/{cmd_id}_stdout.txt", "w")
exit_code_file = open(f"output/{cmd_id}_exit_code.txt", "w")
cmd_output = subprocess.run(
    ["timeout", f"{timeout}", "bash", bash_file_name], stdout=stdout_file, stderr=stderr_file, text=True
)

stdout_file.close()
stderr_file.close()
exit_code_file.write(f"{cmd_output.returncode}")
exit_code_file.close()
logging.info(f"Finished cmd_id: {cmd_id}, exit code: {cmd_output.returncode}")
