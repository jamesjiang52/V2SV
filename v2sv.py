import sys
from src import *


if __name__ == "__main__":
    f_name = sys.argv[1]

    # assume the input file is a .v file
    out_f_name = f_name[:-2] + ".sv"
    out_f = open(out_f_name, "w+")

    with open(f_name, "r") as f:
        f_string = "\n".join(f.readlines())

    f_modules = f_string.split("endmodule")
    f_modules = [module_string + "endmodule" for module_string in f_modules[:-1]]

    for module_string in f_modules:
        module_string = pre_process(module_string)
        module_string = replace_with_logic(module_string)
        module_string = replace_always(module_string)
        module_string = replace_localparam(module_string)
        module_string = post_process(module_string)
        out_f.write(module_string + "\n")

    out_f.close()
