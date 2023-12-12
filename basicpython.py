print("# Basic Python v1")
# added "new" command
# auto renumbers to count line numbers by 10 so there is room to insert a line
# example: line 11 will insert between 10 and 20
# issue: when typing in consecutive lines, the numbers get changed after every line,
#        so entering in lines 1 then 2 then 11 will insert the third line between 1 and 2

program = []
top = {}
no_ready = False

while True:
    if no_ready:
        line = input()
    else:
        line = input("READY.\n")
    lineno = None
    if " " in line:
        command, remainder = line.split(" ", 1)
        lineno = None
        try:
            lineno = int(command, 10)
        except ValueError:
            pass
    else:
        command = line
    no_ready = False
    if lineno is not None:
        if lineno < 1:
            print("Line must be 1+")
        else:
            lineno = int(lineno / 10)
            if lineno >= len(program):
                lineno = len(program)
            program.insert(lineno, remainder)
            no_ready = True
    elif command.lower() == "list":
        for i, line in enumerate(program):
            if line:
                print((i+1)*10, line)
    elif command.lower() == "new":
        program = []
    elif command.lower() == "run":
        isolated = {}
        try:
            exec("\n".join(program), isolated, isolated)
        except Exception as e:
            print(e)
    elif command.lower() == "save":
        filename = remainder.strip(" \"")
        with open(filename, "w") as f:
            f.write("\n".join(program))
    elif command.lower() == "load":
        filename = remainder.strip(" \"")
        with open(filename, "r") as f:
            program = f.readlines()
            program = [line.strip("\r\n") for line in program]
    else:
        try:
            exec(line, top, top)
        except Exception as e:
            print(e)

