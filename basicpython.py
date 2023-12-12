print("# Basic Python v1")
# Added "renum" or "renumber" command to enable line inserting (default max = 10);
#     required maintaining a separate line number list; auto-renumbers at load file
# Added "new" command to erase current python program in memory
# Added "ls" or "dir" command to list current directory file list
# Added "rm" or "erase" or "del" or "delete" command to erase a file in the directory
# Added "format" to completely reformat the filesystem: it will erase this file too!
# TODO: Add optional argument to "run" that will load and execute a file
# TODO: Start in a new subdirectory that is created if it does not exist
# TODO: Add change directory, create directory, delete directory (os.rmdir('directory'))

import os # Used for file directory operations

file_path = "."
program = []
line_number = []
top = {}
no_ready = False

while True:
    if no_ready:
        line = input()
    else:
        line = input("READY.\n")
    lineno = None
    remainder = ""
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
            if len(program) == 0:
                line_number = [lineno]
                program = [remainder]
            else:
                # Find where to insert (sorted)
                index = len(line_number)
                for i in range(len(line_number)):
                    if line_number[i] > lineno:
                        index = i
                        break
                # Replace existing line number
                if lineno == line_number[index - 1]:
                    program[index - 1] = remainder
                # Insert new line
                else:
                    line_number.insert(index, lineno)
                    program.insert(index, remainder)
            no_ready = True
    elif command.lower() in {"renum", "renumber"}:
        # Renumber by 10 unless another number <= 10 is specified
        line_skip = 10
        try:
            line_skip = min(int(remainder, 10), 10)
        except ValueError:
            pass
        for i in range(len(program)):
            line_number[i] = (i+1) * line_skip
    elif command.lower() == "list":
        for i, line in enumerate(program):
            if line:
                print("{:>4}".format(line_number[i]), line)
    elif command.lower() == "new":
        program = []
        line_number = []
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
        # create line numbers
        line_number = [0] * len(program)
        for i in range(len(line_number)):
            line_number[i] = (i+1) * 10
    elif command.lower() in {"ls", "dir"}:
        print("Directory " + os.getcwd())
        filelist = os.listdir(file_path)
        for f in filelist:
            print("    ", f)
    elif command.lower() in {"rm", "erase", "del", "delete"}:
        if os.path.isfile(remainder):
            decision = input("\nAre you sure you want to delete \"" + remainder + "\" (y/n)? ")
            if decision.lower() == "y":
                os.remove(remainder)
        else:
            print("File \"" + remainder + "\" does not exist")
    elif command.lower() == "format":
        import storage
        
        decision = input("\nAre you sure you want to format the filesystem (y/n)? ")
        if decision.lower() == "y":
            isolated = {}
            try:
                exec("storage.erase_filesystem()", isolated, isolated)
            except Exception as e:
                print("\nReformat failed: ERROR " + e)
    else:
        try:
            exec(line, top, top)
        except Exception as e:
            print(e)

