import subprocess
import time

start = time.time()

subprocess.run(["python", "automaton.py"])

subprocess.run(["python", "monitoring.py"], capture_output=True, text=True) 

subprocess.run(["python", "surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
