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
        #We would not need the "if", if we had a Machinetype String to each log!
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
output_seen = [False] * len(machine_log)
for i, user_entry in enumerate(user_log):
        if input_seen[i]:
            continue
        input_seen[i] = True
        output_found = False 
        output_timestamp = i
        input_sequence = user_entry
        output_sequence = []

        input_time = i
        
        if user_entry != ".": # then output expected by user
            for j in range(i, min(i+6, len(user_log))):
                 machine_entry = machine_log[j]

                # If we had input and output and now there is another input: New event!
                 if output_found and user_log[j] != ".":
                     break
                 
                 # If we find more inputs before seeing an output: Input sequence
                 if  j>i and user_log[j] != ".":
                     input_sequence = '{},{}'.format(input_sequence, user_log[j])
                     input_seen[j] = True
                     input_time = j
                 
                 # If we find an output: Output_sequence (And do not break since there might be more outputs)
                 if machine_entry != ".":
                    if  not output_found: #First output to be found
                        output_sequence = machine_entry
                        output_found = True
                        output_seen[j] = True 
                        output_time = j  # For computing time between last input and first output
                        output_timestamp = j  # Timestamp of event is the timestamp of latest output
                    elif(machine_machinetype[j] == machine_machinetype[output_timestamp]):
                        output_sequence = '{},{}'.format(output_sequence, machine_entry)
                        output_seen[j] = True 
                        output_timestamp = j  # Timestamp of event is the timestamp of latest output
                    
                 

            if not output_found:
                input_output.append('({}_{});{};x'.format(input_sequence, ".", user_time[i])) # if there was no concrete output action
            else:
                input_output.append('({}_{});{};x'.format(input_sequence, output_sequence, machine_time[output_timestamp], output_time-input_time))
        
        if(not output_seen[i] and machine_log[i] != "."):
            output_sequence = machine_log[i]
            output_seen[i] = True
            for j in range(i+1, min(i+6, len(user_log))):
                if user_log[j] != ".":
                    break
                if machine_log[j] != "." and machine_machinetype[j] == machine_machinetype[i]:
                     output_sequence = '{},{}'.format(output_sequence, machine_log[j])
                     output_seen[j] = True
            input_output.append('({}_{});{};x'.format(".", output_sequence, machine_time[i]))


        multiuser_entry = multiuser_log[i]
        if "." != multiuser_entry:
            if (multiuser_machinetype[i] == user_machinetype[i]):
                if user_entry ==".": #interacting with the same machine but in the same moment doing nothing
                    input_output.append('({}_{});{};x'.format("Interacting with " + multiuser_machinetype[i],
                                                               multiuser_entry, multiuser_time[i]))
                else:
                    input_output.append('({}_{});{};x'.format(user_entry, multiuser_entry, multiuser_time[i])) 
            #Or user is not doing anything at all or interacting with another machine    
            else: # If user interacts with another machine, the multiuser event is seen independently
                input_output.append('({}_{});{};x'.format(multiuser_machinetype[i], multiuser_entry, multiuser_time[i]))  

with open("input_output.txt", "w") as file:
    for item in input_output:
        file.write("%s\n" % item)