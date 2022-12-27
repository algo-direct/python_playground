from datetime import datetime

print("hello from docker..")
for x in range(1, 1000):
    dt = datetime.strptime("20220606 09:08  IST", "%Y%m%d %H:%M %Z")
