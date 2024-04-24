import subprocess
import time

start = time.time()

subprocess.run(["python", "Macedo\\automaton.py"])

subprocess.run(["python", "Macedo\\mapping.py"], capture_output=True, text=True) 

subprocess.run(["python", "Macedo\\surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
