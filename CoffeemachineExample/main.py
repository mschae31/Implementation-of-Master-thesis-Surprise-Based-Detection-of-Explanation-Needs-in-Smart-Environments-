import subprocess
import time

#Start to run all components subsequently. Alternatively only start surpriseMachine and use
# "Scenario.txt" as simulated data to obtain the results presented in the thesis

start = time.time()

subprocess.run(["python", "CoffeemachineExample\\automaton.py"])

subprocess.run(["python", "CoffeemachineExample\\mapping.py"], capture_output=True, text=True) 

subprocess.run(["python", "CoffeemachineExample\\surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
