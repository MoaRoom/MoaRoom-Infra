#!/usr/bin/python3
import numpy as np
import sys

port_list = np.array([False]*65535)
np.save(f"{sys.argv[1]}/port_list", port_list)
print(f"{sys.argv[1]}/port_list made")
