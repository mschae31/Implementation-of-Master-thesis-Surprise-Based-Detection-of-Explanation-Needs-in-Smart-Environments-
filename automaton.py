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

logger_multiuser = logging.getLogger('multiuser')
logger_multiuser.setLevel(logging.INFO)
handler_multiuser = logging.FileHandler('multiuser.log', mode='w')
handler_multiuser.setFormatter(logging.Formatter('%(message)s'))
logger_multiuser.addHandler(handler_multiuser)
 

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
            logger_machine.info(f"., {env.now}")
            CoffeeMachine.power_ison = True
            yield self.env.timeout(1)
        
        logger_user.info(f"Pressing the button to start Coffeemachine, {env.now}, Coffeemachine")
        logger_machine.info(f"., {env.now}")

        for _ in range(random.randint(1,3)):  # It takes 1 to 3 seconds until the machine starts
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}")
            logger_user.info(f"., {env.now}, Coffeemachine")  #replace by "Test" to check if the several Input combination works

        yield self.env.timeout(1)
        logger_user.info(f"., {env.now}, Coffeemachine")
        logger_machine.info(f"Starting the brewing, {env.now}, Coffeemachine")

        for _ in range(10):
            yield self.env.timeout(1)

            if random.random() < 0.002:
                logger_user.info(f"Waiting, {env.now}, Coffeemachine")
                logger_machine.info(f"Stopping, {env.now}, Coffeemachine")
                self.interaction_active = False
                return
            elif random.random() < 0.05:
                logger_user.info(f"Pressing button to stop, {env.now}, Coffeemachine")
                logger_machine.info(f"Stopping, {env.now}, Coffeemachine")
                self.interaction_active = False
                return
            else:
                logger_user.info(f"Waiting, {env.now}, Coffeemachine")
                logger_machine.info(f"Brewing, {env.now}, Coffeemachine")

        yield self.env.timeout(1)
        logger_machine.info(f"Coffee finished, {env.now}, Coffeemachine")
        logger_user.info(f"Taking the coffee, {env.now}, Coffeemachine")
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Coffeemachine makes a sound, {env.now}, Coffeemachine")


class Mixer(Machine):
    def __init__(self, env, name):
        super().__init__(env, name)
        self.mixed = 0

    def operation(self):
        
        logger_user.info(f"Pressing the button to start Mixer, {env.now}, Mixer")
        logger_machine.info(f"., {env.now}")
        for _ in range(random.randint(1,2)):  # It takes 1 to 2 seconds until the machine starts
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}")
            logger_user.info(f"., {env.now}, Mixer")

        yield self.env.timeout(1)
        logger_user.info(f"., {env.now}, Mixer")
        logger_machine.info(f"Starting the mixing, {env.now}, Mixer")
        for _ in range(3):
            yield self.env.timeout(1)
            if random.random() < 0.01:
                logger_machine.info(f"Turning off, {env.now}, Mixer")
                logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")
                self.interaction_active = False
                return
            else:
                logger_machine.info(f"Mixing, {env.now}, Mixer")
                logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")

        yield self.env.timeout(1)
        logger_machine.info(f"Mixer finished, {env.now}, Mixer")
        logger_user.info(f"Taking the mixed, {env.now}, Mixer")
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Mixer makes a sound, {env.now}, Mixer")

class Lightswitch(Machine):
    def __init__(self, env, name):
        super().__init__(env, name)
        self.lightson = False

    def operation(self):
        if self.lightson:
            logger_user.info(f"Turning lights off, {env.now}, Lightswitch")
            logger_machine.info(f"Lights turn off, {env.now}, Lightswitch")
            self.lightson = False
        else:
            logger_user.info(f"Turning lights on, {env.now}, Lightswitch")
            logger_machine.info(f"Lights turn on, {env.now}, Lightswitch")
            self.lightson = True
        yield self.env.timeout(0)
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Light turns red, {env.now}, Lightswitch")

class Fan(Machine):
    
    def __init__(self, env, name):
        super().__init__(env, name)
        self.on = False
        self.temperature = 15

    """def operation(self):
        print(f"now, {env.now}")
        yield self.env.timeout(1)"""
    
    def operation(self):
        # Nothing, since the Fan works automatically!
        print("This method should not be called!!")
        yield self.env.timeout(0)
        self.interaction_active = False

    def temp_check(self):
        self.temperature = np.clip(np.random.normal(self.temperature, 0.1), -10, 40)
        #print(str(self.temperature)+ " " + str(env.now))
        if (self.temperature>20 and not self.on):
            logger_multiuser.info(f"Fan goes on, {env.now}")
            self.on = True
            
        elif (self.temperature<=20 and self.on):
            logger_multiuser.info(f"Fan goes off, {env.now}")
            self.on = False
        else:
            logger_multiuser.info(f"., {env.now}")
        
        self.interaction_active = False
        

    def multiuser_operation(self):
        logger_multiuser.info(f"Fan makes a sound, {env.now}")


def user_interaction_sequence(env, machines):
    while True:
        yield env.timeout(1)

        #Power is switched off automatically each 100 time units
        if env.now % 100 == 0:
            CoffeeMachine.power_ison =False
        
        if not any(machine.interaction_active for machine in machines):
            selected_machine = random.choice([machine for machine in machines if machine != fan])
            if random.random() < 0.3:
                selected_machine.interaction_active = True
                env.process(selected_machine.operation())
            else:
                logger_user.info(f"., {env.now}")
                logger_machine.info(f"., {env.now}")

        
        # MULTIUSER
        if random.random() < 0.01:
            #inactive_machines = [machine for machine in machines if not machine.interaction_active]
            selected_machine = random.choice(machines)
            selected_machine.multiuser_operation()
        else: #Check always for fan temperature (just not in the same moment as there is multiuser action)
            fan.temp_check()    

        # ENVIRONMENTAL
        #fan.temp_check()      

# Create environment
env = simpy.Environment()

# Create machines
coffee_machine = CoffeeMachine(env, "Coffee Machine")
mixer = Mixer(env, "Mixer")
lightswitch = Lightswitch(env, "Lightswitch")
fan = Fan(env, "Fan")

# Start interaction
env.process(user_interaction_sequence(env, [coffee_machine, mixer, lightswitch, fan]))

# Start simulation
env.run(until=50000)  # Indicate number of time units


