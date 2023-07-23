
echo "================="
id
whoami
echo "================="
exec sudo -u invaeg_bm_1 /bin/sh - << eof
id
git pull origin main
eof
