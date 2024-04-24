import subprocess
import time

start = time.time()

subprocess.run(["python", "Bayesian\\automaton.py"])

subprocess.run(["python", "Bayesian\\mapping.py"], capture_output=True, text=True) 

subprocess.run(["python", "Bayesian\\surpriseMachine.py"])

end = time.time()

time = end - start

print(f'The execution time is {time}s')
