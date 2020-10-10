from common import *

#f_name = "verilog/divider_wrapper.v"
#f_name = "verilog/divider.v"
#f_name = "verilog/divider_controlpath.v"
f_name = "verilog/divider_datapath.v"

with open(f_name, "r") as f:
    f_string = "\n".join(f.readlines())

print(pre_process(f_string, debug=True))
