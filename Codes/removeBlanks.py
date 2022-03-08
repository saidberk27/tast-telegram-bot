def remove_blanks():
    output = ""
    with open("Group List.txt") as f:
        for line in f:
            if not line.isspace():
                output += line

    f = open("Group List.txt", "w")
    f.write(output)