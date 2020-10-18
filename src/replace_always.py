def replace_always(module_string, debug=False):
    buffer = module_string[:module_string.index(");") + 2] + "\n"
    body_string = module_string[module_string.index(");") + 2:]
    statements = body_string.split(";")
    
    for statement in statements:
        words = statement.split()
        if not words:
            continue
        if words[0] == "always":
            new_words = words[:]
            if words[1] == "@*":
                sensitivity_list = "*"
            else:
                sensitivity_list = statement[statement.index("@(") + 2:statement.index(")")]
            if sensitivity_list == "*":
                # combinational logic, so replace with always_comb
                new_words[0] = "always_comb"
                new_statement = " ".join(new_words)
                buffer += "{};\n".format(new_statement)
                if debug:
                    print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
            elif "posedge" in sensitivity_list or "negedge" in sensitivity_list:
                # register logic, so replace with always_ff
                new_words[0] = "always_ff"
                new_statement = " ".join(new_words)
                buffer += "{};\n".format(new_statement)
                if debug:
                    print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
            else:
                # the sensitivity list is something weird
                # the most likely scenario is that all the signals that are being evaluated in the always block are in the sensitivity list
                # in that case, it's purely combinational logic, so technically we should replace it with always_comb,
                # but that seems complicated to check so I'll just keep the statement as is
                buffer += "{};\n".format(" ".join(words))
        else:
            # don't care at all about anything else
            buffer += "{};\n".format(" ".join(words))
            
    # remove trailing semicolon from endmodule
    if buffer[-2] == ";":
        buffer = buffer[:-2] + "\n"

    return buffer
