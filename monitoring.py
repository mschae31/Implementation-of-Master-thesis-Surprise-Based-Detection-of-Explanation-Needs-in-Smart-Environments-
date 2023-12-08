def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    log_list = []
    timestamp_list = []
    machinetype_list = []
    
    for line in lines:
        parts = [x.strip() for x in line.split(',')]
        logs = parts[0].strip()
        timestamp = parts[1].strip()
        #We do not need the following if we had a Machine String to each log!
        if len(parts) >= 3:
            machine = parts[2].strip()
        else:
            machine = ""

        log_list.append(logs)
        timestamp_list.append(timestamp)
        machinetype_list.append(machine)

    return log_list, timestamp_list, machinetype_list

machine_log, machine_time, machine_machinetype = read_log_file('machine.log')

user_log, user_time, user_machinetype = read_log_file('user.log')

multiuser_log, multiuser_time, multiuser_machinetype = read_log_file('multiuser.log')

input_output = []
#before time was included and assigning points from different timestamps was necessary:
"""for user_entry, machine_entry, multiuser_entry in zip(user_log, machine_log, multiuser_log ):

    if "Doing nothing" == user_entry and "" != multiuser_entry:
        input_output.append('({},{})'.format(user_entry, multiuser_entry))
    else:
        input_output.append('({},{})'.format(user_entry, machine_entry))"""

# with time:
    #search for an input and then find the corresponding output in another for loop

input_seen = [False] * len(user_log)  # Set True if a specific input has already been taken into account
for i, user_entry in enumerate(user_log):
        if input_seen[i]:
            continue
        input_seen[i] = True
        output_found = False 
        input_sequence = user_entry
        
        if user_entry != ".": # then output expected by user
            for j in range(i, min(i+6, len(user_log))):
                 machine_entry = machine_log[j]

                 if  j>i and user_log[j] != ".":
                     input_sequence = '{},{}'.format(input_sequence, user_log[j])
                     input_seen[j] = True
                 
                 if machine_entry != ".":
                    input_output.append('({}_{});{}'.format(input_sequence, machine_entry, machine_time[j]))
                    output_found = True
                    break
                 
            if not output_found:
                input_output.append('({}_{});{}'.format(user_entry, ".", user_time[i])) # if there was no concrete output action
        multiuser_entry = multiuser_log[i]
        if "." != multiuser_entry and (multiuser_machinetype[i] == user_machinetype[i] or user_entry == "."):
            input_output.append('({}_{});{}'.format(user_entry, multiuser_entry, multiuser_time[i]))     

with open("input_output.txt", "w") as file:
    for item in input_output:
        file.write("%s\n" % item)