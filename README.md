# Masterthesis


Execute main.py within one of the model folders (Bayesian, CCS, Macedo, Shannon) to start the following process:

1) Simulate the interaction of a user with smart home and collect seperately the data of what the user and machine do in each second -> Log files: "user", "machine", "external"

2) Transfer these data to the mapping unit that assigns inputs (user's actions) to the corresponding output (machine's reaction) based on specific rules. We get datapoints of "events" for each second -> Event file "input_output.txt"

3) Apply the mathematical model of Surprise on these datapoints to decide which event was surprising for the user.
4) Output all surprising event with details about input/output, time and amount of surprise. Show plots


