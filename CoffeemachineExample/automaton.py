import simpy
import random
import logging
import numpy as np

logger_machine = logging.getLogger('machine')
logger_machine.setLevel(logging.INFO)
handler_machine = logging.FileHandler('machine.log', mode='w')
handler_machine.setFormatter(logging.Formatter('%(message)s'))
logger_machine.addHandler(handler_machine)

logger_user = logging.getLogger('user')
logger_user.setLevel(logging.INFO)
handler_user = logging.FileHandler('user.log', mode='w')
handler_user.setFormatter(logging.Formatter('%(message)s'))
logger_user.addHandler(handler_user)

logger_external = logging.getLogger('external')
logger_external.setLevel(logging.INFO)
handler_external = logging.FileHandler('external.log', mode='w')
handler_external.setFormatter(logging.Formatter('%(message)s'))
logger_external.addHandler(handler_external)
 

class Machine:
    def __init__(self, env, name):
        self.env = env
        self.process = None
        self.name = name
        self.interaction_active = False

    def operation(self):
        raise NotImplementedError("Subclasses must implement this method")


class CoffeeMachine(Machine):

    power_ison = False       #Power in the room has to be turned on by a switch

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        if not CoffeeMachine.power_ison:
            logger_user.info(f"Switching power on, {env.now}, Coffeemachine")
            logger_machine.info(f"., {env.now}, Coffeemachine")
            logger_external.info(f"., {env.now}, Coffeemachine") 
            CoffeeMachine.power_ison = True
            yield self.env.timeout(1)
        
        logger_user.info(f"Pressing the button to start Coffeemachine, {env.now}, Coffeemachine")
        logger_machine.info(f"., {env.now}, Coffeemachine")
        logger_external.info(f"., {env.now}, Coffeemachine")

        for _ in range(random.randint(1,3)):  # It takes 1 to 3 seconds until the machine starts
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}, Coffeemachine")
            logger_user.info(f"., {env.now}, Coffeemachine") 
            logger_external.info(f"., {env.now}, Coffeemachine")    

        yield self.env.timeout(1)
        logger_user.info(f"., {env.now}, Coffeemachine")
        logger_machine.info(f"Starting the brewing, {env.now}, Coffeemachine")
        logger_external.info(f"., {env.now}, Coffeemachine")

        for _ in range(10):
            yield self.env.timeout(1)

            if random.random() < 0.01:
                logger_user.info(f"Waiting for Coffeemachine, {env.now}, Coffeemachine")
                logger_machine.info(f"., {env.now}, Coffeemachine")
                logger_external.info(f"Stopping, {env.now}, Coffeemachine")
                self.interaction_active = False
                return
            elif random.random() < 0.05:
                logger_user.info(f"Pressing button to stop, {env.now}, Coffeemachine")
                logger_machine.info(f"Stopping, {env.now}, Coffeemachine")
                logger_external.info(f"., {env.now}, Coffeemachine")
                self.interaction_active = False
                return
            else:
                logger_user.info(f"Waiting for Coffeemachine, {env.now}, Coffeemachine")
                logger_machine.info(f"Brewing, {env.now}, Coffeemachine")
                logger_external.info(f"., {env.now}, Coffeemachine")

        yield self.env.timeout(1)
        if env.now < 20000:
             logger_machine.info(f"Coffee ready sound, {env.now}, Coffeemachine")
        else:   #Rule change
            logger_machine.info(f"New coffee ready sound, {env.now}, Coffeemachine")
        logger_user.info(f"Taking the coffee, {env.now}, Coffeemachine")
        logger_external.info(f"., {env.now}, Coffeemachine")
        self.interaction_active = False



def user_interaction_sequence(env, machines):
    while True:
        yield env.timeout(1)

        #Power is switched off automatically each 100 time units
        if env.now % 100 == 0:
            CoffeeMachine.power_ison = False
        
        if not any(machine.interaction_active for machine in machines):
            selected_machine = random.choice([machine for machine in machines]) #if machine != fan])
            if random.random() < 0.3:
                selected_machine.interaction_active = True
                env.process(selected_machine.operation())
            else:
                logger_user.info(f"., {env.now}")
                logger_machine.info(f"., {env.now}")
                logger_external.info(f"., {env.now}")

         

# Create environment
env = simpy.Environment()

# Create machine
coffee_machine = CoffeeMachine(env, "Coffee Machine")

# Start interaction
env.process(user_interaction_sequence(env, [coffee_machine]))

# Start simulation
env.run(until=4000)  # Indicate number of time units


