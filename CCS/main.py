import subprocess
import time

start = time.time()

subprocess.run(["python", "CCS\\automaton.py"])

subprocess.run(["python", "CCS\\mapping.py"], capture_output=True, text=True) 

subprocess.run(["python", "CCS\\surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
