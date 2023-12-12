print("# Basic Python v1")

program = []
new_program = []
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
            if lineno >= len(program):
                program.extend([""] * (lineno - len(program)))
            program[lineno - 1] = remainder
            no_ready = True
    elif command.lower() == "renum":
        # move program lines into every 10 position in the array to allow for code insert
        new_program.extend([""] * 10 * (1 + len(program)))
        i = 1
        for j, line in enumerate(program):
            if line:
                new_program[i*10 - 1] = line
                i += 1
        if len(new_program) > 0:
            program = new_program
    elif command.lower() == "list":
        for i, line in enumerate(program):
            if line:
                print(i+1, line)
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

