# replaces end with end;
# so the subsequent line will be treated as a new statement
# kind of a hack, but oh well
def __replace_end(module_string, debug=False):
    buffer = module_string[:module_string.index(");") + 2] + "\n"
    body_string = module_string[module_string.index(");") + 2:]
    
    idx = 0
    while idx < len(body_string):
        if body_string[idx:idx + 3] == "end":
            # need to check if endcase, endgenerate, or endmodule
            # check from shortest to longest to avoid IndexErrors
            if body_string[idx + 4].isspace() and body_string[idx - 1].isspace():
                # regular end
                buffer += "end;\n"
                if debug:
                    print("Replaced end with end;\n\n")
                idx += len("end;")
            elif body_string[idx + 3:idx + 3 + len("case")] == "case" and body_string[idx - 1].isspace():
                buffer += "endcase;\n"
                if debug:
                    print("Replaced endcase with endcase;\n\n")
                idx += len("endcase;")
            elif body_string[idx + 3:idx + 3 + len("module")] == "module" and body_string[idx - 1].isspace():
                # can just break if endmodule
                buffer += "endmodule\n"
                return buffer
            elif body_string[idx + 3:idx + 3 + len("generate")] == "generate" and body_string[idx - 1].isspace():
                buffer += "endgenerate;\n"
                if debug:
                    print("Replaced endgenerate with endgenerate;\n\n")
                idx += len("endgenerate;")
            else:
                # end/endcase/endmodule/endgenerate is part of the variable name
                buffer += body_string[idx]
                idx += 1
        else:
            buffer += body_string[idx]
            idx += 1
                
    # shouldn't ever get here, if Verilog syntax was correct
    raise ValueError("Expected 'endmodule' at end of module")
    

def pre_process(module_string, debug=False):
    module_string = __replace_end(module_string, debug=debug)
    
    return module_string
