import simpy
import random
import logging

logger_machine = logging.getLogger('coffeemachine')
logger_machine.setLevel(logging.INFO)
handler_machine = logging.FileHandler('coffeemachine.log', mode='w')
handler_machine.setFormatter(logging.Formatter('%(message)s'))
logger_machine.addHandler(handler_machine)

logger_user = logging.getLogger('user')
logger_user.setLevel(logging.INFO)
handler_user = logging.FileHandler('user.log', mode='w')
handler_user.setFormatter(logging.Formatter('%(message)s'))
logger_user.addHandler(handler_user)


class Coffeemachine:
    def __init__(self, env):
        self.env = env
        self.brewing = None
        self.done = 0
        self.failCount = 0
        self.fail = False
        self.manualStopCount = 0
        self.manualStop = False
        self.brewing_active = False  
        self.coffee_done = False

    def brewing_coffee(self):
        self.brewing_active = True
        logger_machine.info(f"Starting the brewing")
        
        try:
            yield self.env.timeout(10)
        except simpy.Interrupt as interrupt:
            if interrupt.cause != "Stop":
                raise

        if not (self.fail or self.manualStop):
            logger_machine.info(f"Coffee finished")
            logger_user.info(f"Taking the coffee")
            self.done += 1
            self.coffee_done = True
        else:
            self.fail = False
            self.manualStop = False

        self.brewing_active = False

    def user_interaction(self):
        while True:
            yield self.env.timeout(1)
            # Skip one iteration if coffee is done (Since more should not happen in one time unit)
            if self.coffee_done:
                self.coffee_done = False
                continue    
            if not self.brewing_active:
                if random.random() < 0.5:
                    logger_user.info(f"Pressing button to start")
                    self.brewing = self.env.process(self.brewing_coffee())
                else:
                    logger_user.info(f"Doing nothing")
                    logger_machine.info(f"Doing nothing")

            else:
                stop_probability = random.random()
                if stop_probability < 0.002:
                    logger_user.info(f"Waiting")
                    logger_machine.info(f"Stopping")
                    self.failCount += 1
                    self.fail = True
                    self.brewing.interrupt(cause="Stop")
                    self.brewing_active = False
                elif stop_probability < 0.05:
                    logger_user.info(f"Pressing button to stop")
                    logger_machine.info(f"Stopping")
                    self.manualStopCount += 1
                    self.manualStop = True
                    self.brewing.interrupt(cause="Stop")
                    self.brewing_active = False
                else:
                    logger_user.info(f"Waiting")
                    logger_machine.info(f"Brewing")


# Create environment
env = simpy.Environment()

# Create coffeemachine
maschine = Coffeemachine(env)

# Start user interaction
env.process(maschine.user_interaction())

# Start simulation
env.run(until=8000)  # Indicate number of time units

# Print Counts
print("Coffees made:", maschine.done)
print("Fail stops:", maschine.failCount)
print("Manual stops:", maschine.manualStopCount)