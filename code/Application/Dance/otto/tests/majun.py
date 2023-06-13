"""
Otto All moves python test 
OttDIY Python Project, 2020 | sfranzyshen
"""
import time
import ottolib.otto9 as otto9

Otto = otto9.Otto9()
# Otto.init(5, 12, 13, 14, True, 0, 1, 2, 3)
# Otto.init(5, 4, 0, 2, True, -1, -1, -1, -1)
#Otto.init(12, 11, 9, 7, True, -1, -1, -1, -1)  # s2 mini + IO shield pins
Otto.init(12, 11, 9, 7, True, -1, -1, -1, -1, 33, 35)  # s2 mini + IO shield pins
# Otto.initHUMANOID(14, 12, 13, 15, 5, 4, True, -1, -1, -1, -1) # d1 mini pins
# Otto.initHUMANOID(7, 9, 11, 12, 35, 33, True, -1, -1, -1, -1)  # s2 mini + IO shield pins
Otto.home()
Otto.walk(2, 1000, 1)  # -- 2 steps, "TIME". IF HIGHER THE VALUE THEN SLOWER (from 600 to 1400), 1 FORWARD
Otto.walk(2, 1000, 1)  # -- 2 steps, "TIME". IF HIGHER THE VALUE THEN SLOWER (from 600 to 1400), 1 FORWARD
Otto.walk(2, 1000, 1)  # -- 2 steps, "TIME". IF HIGHER THE VALUE THEN SLOWER (from 600 to 1400), 1 FORWARD