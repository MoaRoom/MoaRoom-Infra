#!/usr/bin/python3
import numpy as np
import sys

port_list = np.array([False]*65535)
np.save("%s/port_list" % sys.argv[1], port_list)
print("%s/port_list made" % sys.argv[1])
