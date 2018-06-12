import os
import time
start_time = time.time()
while ((time.time() - start_time) <= 15):
    pass
print(os.popen("ps -ax").read())
