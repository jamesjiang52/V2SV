from common import pre_process
from replace_with_logic import replace_with_logic

#f_name = "verilog/divider_wrapper.v"
#f_name = "verilog/divider.v"
#f_name = "verilog/divider_controlpath.v"
f_name = "verilog/divider_datapath.v"

with open(f_name, "r") as f:
    f_string = "\n".join(f.readlines())

print(replace_with_logic(pre_process(f_string), debug=True))
