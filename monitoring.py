def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

coffeemachine_log = read_log_file('coffeemachine.log')

user_log = read_log_file('user.log')


#print(user_log)

input_output = ['({},{})'.format(user_entry, machine_entry) for user_entry, machine_entry in zip(user_log, coffeemachine_log)]

print(input_output)
print("Monitoring worked")
with open("input_output.txt", "w") as file:
    for item in input_output:
        file.write("%s\n" % item)