def __replace_with_logic_header(header_string, debug=False):
    buffer = ""
    IOs = header_string.split(",")
    for IO in IOs:
        words = IO.split()
        if not words:
            continue
        if words[0] == "input":
            # don't care about inputs, so just write it back
            buffer += "{},\n".format(" ".join(words))
        elif words[0] == "output":
            # make a copy so we have the original words for debugging
            new_words = words[:]
            # replace reg and wire with logic
            if "reg" in words:
                new_words[words.index("reg")] = "logic"
            elif "wire" in words:
                new_words[words.index("wire")] = "logic"
            else:
                # reg or wire not specified
                # default type is wire, so insert logic after output
                new_words.insert(1, "logic")
            new_IO = " ".join(new_words)
            buffer += "{},\n".format(new_IO)
            if debug:
                print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_IO))
        else:
            # IO is declared as input or output later, so just write it back
            buffer += "{},\n".format(" ".join(words))

    # remove trailing comma from last IO
    if buffer[-2] == ",":
        buffer = buffer[:-2] + "\n"

    return buffer


def __replace_with_logic_body(body_string, debug=False):
    buffer = ""
    statements = body_string.split(";")
    for statement in statements:
        words = statement.split()
        if not words:
            continue
        if words[0] == "input":
            # don't care about inputs, so just write it back
            buffer += "{};\n".format(" ".join(words))
        elif words[0] == "output":
            # make a copy so we have the original words for debugging
            new_words = words[:]
            # replace reg and wire with logic
            if "reg" in words:
                new_words[words.index("reg")] = "logic"
            elif "wire" in words:
                new_words[words.index("wire")] = "logic"
            else:
                # reg or wire not specified
                # default type is wire, so insert logic after output
                new_words.insert(1, "logic")
            new_statement = " ".join(new_words)
            buffer += "{};\n".format(new_statement)
            if debug:
                print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
        elif words[0] == "reg":
            # make a copy so we have the original words for debugging
            new_words = words[:]
            # replace reg with logic
            new_words[0] = "logic"
            new_statement = " ".join(new_words)
            buffer += "{};\n".format(new_statement)
            if debug:
                print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
        elif words[0] == "wire":
            if "=" in statement:
                # assignment is on same line as declaration, so need to split into two lines
                if ":" in words[1]:
                    # wire is an array
                    signal = word[2]
                else:
                    signal = word[1]
                # first line is declaration using logic
                first_line_words = statement[:statement.index("=")].split()
                first_line_words[0] = "logic"
                new_statement_1 = " ".join(first_line_words)
                # second line is assignment
                second_line_words_append = statement[statement.index("=") + 1:]
                new_statement_2 = "assign {} = {}".format(signal, " ".join(second_line_words_append))
                buffer += "{};\n{};\n".format(new_statement_1, new_statement_2)
                if debug:
                    print("Replaced:\n{}\nwith\n{}\n{}\n\n".format(" ".join(words), new_statement_1, new_statement_2))
            else:
                new_words = words[:]
                # can just replace with logic if no assignment
                new_words[0] = "logic"
                new_statement = " ".join(new_words)
                buffer += "{};\n".format(new_statement)
                if debug:
                    print("Replaced:\n{}\nwith\n{}\n\n".format(" ".join(words), new_statement))
        else:
            # don't care at all about anything else
            buffer += "{};\n".format(" ".join(words))

    # remove trailing semicolon from endmodule
    if buffer[-2] == ";":
        buffer = buffer[:-2] + "\n"

    return buffer

# FIXME: doesn't account for comments
def replace_with_logic(module_string, debug=False):
    new_header_string = __replace_with_logic_header(module_string[module_string.index("(") + 1:module_string.index(");")], debug=debug)
    new_body_string = __replace_with_logic_body(module_string[module_string.index(");") + 2:], debug=debug)
    new_module_string = "{}(\n{});\n{}\n".format(module_string[:module_string.index("(")], new_header_string, new_body_string)

    return new_module_string
