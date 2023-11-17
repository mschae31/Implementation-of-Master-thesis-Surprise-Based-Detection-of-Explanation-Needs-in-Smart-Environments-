import subprocess

subprocess.run(["python", "automaton.py"])

subprocess.run(["python", "monitoring.py"], capture_output=True, text=True)

subprocess.run(["python", "surpriseMachine.py"])
