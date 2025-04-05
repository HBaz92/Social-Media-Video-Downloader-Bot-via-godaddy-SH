# create a file named force_update.py
import os
import time

# Touch the restart.txt file to trigger a Passenger restart
with open("tmp/restart.txt", "w") as f:
    f.write(str(time.time()))
print("Restart file updated. Application should restart within a minute.")
