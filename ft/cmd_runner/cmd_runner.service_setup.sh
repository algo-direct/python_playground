sudo systemctl stop cmd_runner
sudo cp cmd_runner.service /lib/systemd/system/
sudo systemctl disable cmd_runner
sudo systemctl enable cmd_runner
sudo systemctl start cmd_runner
sudo systemctl status cmd_runner
