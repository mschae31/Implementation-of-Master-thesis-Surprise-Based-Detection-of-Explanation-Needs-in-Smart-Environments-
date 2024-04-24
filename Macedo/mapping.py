# Read the data streams
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
        #We would not need the following, if we had a Machinetype String to each log!
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

external_log, external_time, external_machinetype = read_log_file('external.log')

input_output = []


input_seen = [False] * len(user_log)  # Set True if a specific input has already been taken into account
output_seen = [False] * len(machine_log)

#Data Mapping, iterate through the inputs:
for i, user_entry in enumerate(user_log):
        if input_seen[i]:
            continue
        input_seen[i] = True
        output_found = False 
        output_timestamp = i
        input_sequence = user_entry
        output_sequence = []

        input_time = i
        
        if user_entry != ".": # If input given, then output expected by user
            for j in range(i, min(i+6, len(user_log))): #time window = 5
                 machine_entry = machine_log[j]
                 external_entry = external_log[j]

                # If we had input and output and now there is another input: New event!
                 if output_found and user_log[j] != ".":
                     break
                 
                 # If we find more inputs before seeing an output: Input sequence
                 if  j>i and user_log[j] != ".":
                     input_sequence = '{},{}'.format(input_sequence, user_log[j])
                     input_seen[j] = True
                     input_time = j
                 
                 # If we find an output: Output_sequence (And do not break since there might be more outputs)
                 #First check for external output:
                 if external_entry != ".":
                    if  not output_found: #First output to be found
                        output_sequence = external_entry
                        output_found = True
                        output_seen[j] = True 
                        output_time = j  # For computing time between last input and first output
                        output_timestamp = j  # Timestamp of event is the timestamp of latest output
                    else:
                        output_sequence = '{},{}'.format(output_sequence, external_entry)
                        output_seen[j] = True 
                        output_timestamp = j  # Timestamp of event is the timestamp of latest output
                 elif machine_entry != ".":
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
                    
                 
            # No Output
            if not output_found:
                input_output.append('({}_{});{};x'.format(input_sequence, ".", user_time[i]))
            # Output found
            else:
                input_output.append('({}_{});{};{}'.format(input_sequence, output_sequence, machine_time[output_timestamp], output_time-input_time))
        
        # Since we iterate through inputs, we have to check whether we did not cover an output (No input event)
        #External output:
        if(not output_seen[i] and external_log[i] != "."):
            output_sequence = external_log[i]
            output_seen[i] = True
            for j in range(i+1, min(i+6, len(user_log))):
                if user_log[j] != ".":
                    break
                if external_log[j] != ".":
                     output_sequence = '{},{}'.format(output_sequence, external_log[j])
                     output_seen[j] = True
            input_output.append('({}_{});{};x'.format(".", output_sequence, external_time[i]))
        # "Normal" output
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


with open("input_output.txt", "w") as file:
    for item in input_output:
        file.write("%s\n" % item)