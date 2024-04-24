import subprocess
import time

start = time.time()

subprocess.run(["python", "Shannon\\automaton.py"])

subprocess.run(["python", "Shannon\\mapping.py"], capture_output=True, text=True) 

subprocess.run(["python", "Shannon\\surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
