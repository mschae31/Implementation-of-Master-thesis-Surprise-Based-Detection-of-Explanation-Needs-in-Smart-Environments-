Brief documentation of what is implemented in which folder:

- Bayesian, CCS, Macedo, Shannon: Implementation of the mathematical surprise model, respectively (surpriseMachine.py) and a simulation (automaton.py) + event assignment (mapping.py) implementation. See master thesis for background. Note, an examplary Gaussian surprise implementation is included in each surpriseMachine.py.
- CoffeemachineExample: Implementation of the running example in master thesis chapter 4. Including the used simulated data (Scenario.txt). Copy Scenario.txt in input_output.txt to repeat the results from the thesis. 
- Evaluation: Creation of the plots for the evaluation chapter.
- Gaussian: Creation of a plot.
- MonitoringPlots: Creation of the plots for chapter 4.
- PlotsBayesianExtenstion: Creation of plots for several chapters.

FILES:
- external.log, machine.log, user.log are the three logs obtained by the first component. See thesis for details. If new data are simulated (e.g., by starting a main.py in one of the four model folders), the logs are updated.
- input_output.txt: Assigned events obtained by inserting the three log files in the mapping component. Insert your own event data here for testing! See thesis for details.