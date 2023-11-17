def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

machine_log = read_log_file('machine.log')

user_log = read_log_file('user.log')

multiuser_log = read_log_file('multiuser.log')

input_output = []
for user_entry, machine_entry, multiuser_entry in zip(user_log, machine_log, multiuser_log ):

    if "Doing nothing" == user_entry and "" is not multiuser_entry:
        input_output.append('({},{})'.format(user_entry, multiuser_entry))
    else:
        input_output.append('({},{})'.format(user_entry, machine_entry))

with open("input_output.txt", "w") as file:
    for item in input_output:
        file.write("%s\n" % item)