def __remove_extra_declarations(module_string, replaced_wires, debug=False):
    buffer = module_string[:module_string.index(");") + 2] + "\n"
    body_string = module_string[module_string.index(");") + 2:]
    statements = body_string.split(";")

    # remove the previous declarations of any new enums
    for statement in statements:
        words = statement.split()
        if not words:
            continue
        if words[0] in ["reg", "wire", "logic"]:
            if ":" in words[1]:
                # wire is an array
                signals = statement[statement.index("]") + 1:].split()
            else:
                signals = words[1:]
                
            signals = [signal[:-1] if signal[-1] == "," else signal for signal in signals]

            signals_remaining = signals[:]
            for signal in signals:
                if signal in replaced_wires:
                    signals_remaining.remove(signal)

            if signals_remaining == signals:
                # none of these signals were changed to enums
                buffer += "{};\n".format(" ".join(words))
            elif signals_remaining == []:
                # all signals are declared as new enums now, so don't write anything
                if debug:
                    print("Removed:\n{}\n\n".format(" ".join(words)))
            else:
                new_statement = "logic "  # might as well do this
                if ":" in words[1]:
                    # wire is an array
                    new_statement += words[1] + " "
                for signal in signals_remaining:
                    new_statement += signal + ", "
                # remove trailing comma from last wire
                if new_statement[-2] == ",":
                    new_statement = new_statement[:-2]

                buffer += "{};\n".format(new_statement)
                if debug:
                    print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
        else:
            # don't care
            buffer += "{};\n".format(" ".join(words))

    # remove trailing semicolon from endmodule
    if buffer[-2] == ";":
        buffer = buffer[:-2] + "\n"

    return buffer


def replace_localparam(module_string, debug=False):
    buffer = module_string[:module_string.index(");") + 2] + "\n"
    body_string = module_string[module_string.index(");") + 2:]
    statements = body_string.split(";")

    replaced_wires = []

    for statement in statements:
        words = statement.split()
        if not words:
            continue
        if words[0] == "localparam":
            new_statement = "enum int unsigned {\n"
            params = []
            pair_strings = "".join(words[1:]).split(",")
            # get all localparam names
            for pair_string in pair_strings:
                param = pair_string.split("=")[0]
                new_statement += param + ",\n"
                params.append(param)
            # remove trailing comma from last param
            if new_statement[-2] == ",":
                new_statement = new_statement[:-2] + "\n} "

            # need to search for wires that are being assigned to these localparams,
            # and declare these as the new enums
            for statement_i in statements:
                if "=" in statement_i or "<=" in statement_i:
                    statement_i = statement_i.replace("<=", "=")
                    words_i = statement_i.split()
                    if words_i[-1] in params:
                        wire = statement_i[:statement_i.index("=")].split()[-1]
                        if wire not in replaced_wires:
                            new_statement += wire + ", "
                            replaced_wires.append(wire)
                else:
                    # don't care
                    pass
            # remove trailing comma from last wire
            if new_statement[-2] == ",":
                new_statement = new_statement[:-2]

            buffer += "{};\n".format(new_statement)
            if debug:
                print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
        else:
            # don't care at all about anything else
            buffer += "{};\n".format(" ".join(words))

    buffer = __remove_extra_declarations(buffer, replaced_wires, debug=debug)

    return buffer
