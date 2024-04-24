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

            if random.random() < 0.002:
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

    def external_operation(self):
        logger_external.info(f"Coffeemachine makes a sound, {env.now}, Coffeemachine")


class Mixer(Machine):

    overheated = False
    last_used = 0
    used_counter = 0

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        
        
        #The user knows more or less how long to wait but sometimes s/he misjudges the time
        if Mixer.overheated and 60 > np.random.normal(min(Mixer.used_counter*10,70), 5): #time misjudge
            logger_user.info(f"Pressing the button to start Mixer, {env.now}, Mixer")
            logger_machine.info(f"Mixer shows a red light, {env.now}, Mixer")
            logger_external.info(f"., {env.now}, Mixer")
            yield self.env.timeout(0)
            self.interaction_active = False
        elif Mixer.overheated: #User knows it is overheated -> no interaction
            logger_user.info(f"., {env.now}")
            logger_machine.info(f"., {env.now}")
            logger_external.info(f"., {env.now}, Mixer")
            self.interaction_active = False
            return
        else:
            logger_user.info(f"Pressing the button to start Mixer, {env.now}, Mixer")
            logger_machine.info(f"Mixer shows a green light, {env.now}, Mixer")
            logger_external.info(f"., {env.now}, Mixer")
            for _ in range(random.randint(1,2)):  # It takes 1 to 2 seconds until the machine starts
                yield self.env.timeout(1)
                logger_machine.info(f"., {env.now}, Mixer")
                logger_user.info(f"., {env.now}, Mixer")
                logger_external.info(f"., {env.now}, Mixer")

            yield self.env.timeout(1)
            logger_user.info(f"., {env.now}, Mixer")
            logger_machine.info(f"Starting the mixing, {env.now}, Mixer")
            logger_external.info(f"., {env.now}, Mixer")
            for _ in range(3):
                yield self.env.timeout(1)
                if random.random() < 0.01:
                    logger_machine.info(f"., {env.now}, Mixer")
                    logger_external.info(f"Turning off, {env.now}, Mixer")
                    logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")
                    Mixer.overheated = True
                    Mixer.last_used = env.now
                    Mixer.used_counter += 1
                    self.interaction_active = False
                    return
                else:
                    logger_machine.info(f"Mixing, {env.now}, Mixer")
                    logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")
                    logger_external.info(f"., {env.now}, Mixer")

            yield self.env.timeout(1)
            logger_machine.info(f"Mixer finished, {env.now}, Mixer")
            logger_user.info(f"Taking the mixed, {env.now}, Mixer")
            logger_external.info(f"., {env.now}, Mixer")
            Mixer.overheated = True
            Mixer.last_used = env.now
            Mixer.used_counter += 1
            self.interaction_active = False
 
    def external_operation(self):
        logger_external.info(f"Mixer makes a sound, {env.now}, Mixer")


        
class TV(Machine):

    on = False

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        
        logger_user.info(f"Turning TV on, {env.now}, TVstereo")
        logger_machine.info(f"., {env.now}, TVstereo")
        logger_external.info(f"., {env.now}, TVstereo")
        
        for _ in range(random.randint(1,3)):  # It takes 1 to 3 seconds until the TV starts
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}, TVstereo")
            logger_user.info(f"., {env.now}, TVstereo")
            logger_external.info(f"., {env.now}, TVstereo")

        yield self.env.timeout(1)
        logger_user.info(f"., {env.now}, TVstereo")
        logger_machine.info(f"TV turns on, {env.now}, TVstereo")
        logger_external.info(f"., {env.now}, TVstereo")
        TV.on = True
        for _ in range(random.randint(1,3)): # Watches TV for 1-3 seconds
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}, TVstereo") #Before: TV on, TV watching but unneccesary to log
            logger_user.info(f"., {env.now}, TVstereo")
            logger_external.info(f"., {env.now}, TVstereo")

        yield self.env.timeout(1)
        logger_machine.info(f"TV turns off, {env.now}, TVstereo")
        logger_user.info(f"Turning TV off, {env.now}, TVstereo")
        logger_external.info(f"., {env.now}, TVstereo")
        TV.on = False
        self.interaction_active = False

    def external_operation(self):
        logger_external.info(f"TV makes a sound, {env.now}, TVstereo")

class Stereo(Machine):
    
    on = False

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        if Stereo.on:
            logger_user.info(f"Turning Stereo off, {env.now}, TVstereo")
            logger_machine.info(f"Stereo turns off, {env.now}, TVstereo")
            logger_external.info(f"., {env.now}, TVstereo")
            Stereo.on = False
        
        elif random.random() <0.10:
            logger_user.info(f"Turning Stereo on, {env.now}, TVstereo")
            logger_machine.info(f", {env.now}, TVstereo")
            logger_external.info(f"Steroe makes an error sound , {env.now}, TVstereo")
        
        else:
            logger_user.info(f"Turning Stereo on, {env.now}, TVstereo")
            logger_machine.info(f"Stereo turns on, {env.now}, TVstereo")
            logger_external.info(f"., {env.now}, TVstereo")
            Stereo.on = True
        yield self.env.timeout(0)
        self.interaction_active = False

    def external_operation(self):
        logger_external.info(f"Stereo makes a sound, {env.now}, TVstereo")




class Lightswitch(Machine):
    def __init__(self, env, name):
        super().__init__(env, name)
        self.lightson = False

    def operation(self):
        if self.lightson:
            logger_user.info(f"Turning lights off, {env.now}, Lightswitch")
            logger_machine.info(f"Lights turn off, {env.now}, Lightswitch")
            logger_external.info(f"., {env.now}, Lightswitch")
            self.lightson = False
        else:
            logger_user.info(f"Turning lights on, {env.now}, Lightswitch")
            logger_machine.info(f"Lights turn on, {env.now}, Lightswitch")
            logger_external.info(f"., {env.now}, Lightswitch")
            self.lightson = True
        yield self.env.timeout(0)
        self.interaction_active = False

    def external_operation(self):
        logger_external.info(f"Light turns red, {env.now}, Lightswitch")


class Fan(Machine):
    
    def __init__(self, env, name):
        super().__init__(env, name)
        self.on = False
        self.temperature = 15
    
    def operation(self):
        self.temperature = np.clip(np.random.normal(self.temperature, 0.5), -10, 40)
        if (self.temperature>20 and not self.on):
            logger_machine.info(f"Fan goes on, {env.now}, Fan")
            self.on = True
            logger_user.info(f"Temperature high, {env.now}, Fan")  
            logger_external.info(f"., {env.now}, Fan")         
        elif (self.temperature<=20 and self.on):
            logger_machine.info(f"Fan goes off, {env.now}, Fan")
            self.on = False
            logger_user.info(f"Temperature low, {env.now}, Fan")
            logger_external.info(f"., {env.now}, Fan")
        elif (not self.on and random.random() <0.01):
            logger_user.info(f"Fail occurs, {env.now}, Fan") # If we assume that user knows about the fail 
            logger_machine.info(f"Fan goes on, {env.now}, Fan") # If we assume that user knows about the fail 
            logger_external.info(f"., {env.now}, Fan")
            self.on = True 
            yield env.timeout(1)
            logger_machine.info(f"Fan goes off, {env.now}, Fan")
            self.on = False
            logger_user.info(f"., {env.now}")
            logger_external.info(f"., {env.now}, Fan")
        else:
            logger_machine.info(f"., {env.now}")
            logger_user.info(f"., {env.now}")
            logger_external.info(f"., {env.now}, Fan")

            
        yield env.timeout(0)
        self.interaction_active = False

    def external_operation(self):
        logger_external.info(f"Fan makes a sound, {env.now}, Fan")


def user_interaction_sequence(env, machines):
    while True:
        yield env.timeout(1)

        #Power is switched off automatically each 100 time units
        if env.now % 100 == 0:
            CoffeeMachine.power_ison = False
        if env.now - Mixer.last_used > 60:
            Mixer.overheated = False
        
        if not any(machine.interaction_active for machine in machines):
            selected_machine = random.choice([machine for machine in machines]) #if machine != fan])
            if random.random() < 0.3:
                selected_machine.interaction_active = True
                env.process(selected_machine.operation())
            else:
                logger_user.info(f"., {env.now}")
                logger_machine.info(f"., {env.now}")
                
                #external while no interaction at all:
                #Note: We did not include external outputs from other devices than user is interacting!
                if random.random() < 0.005:
                    selected_machine = random.choice(machines)
                    selected_machine.external_operation()
                else:
                     logger_external.info(f"., {env.now}")

         

# Create environment
env = simpy.Environment()

# Create machines
coffee_machine = CoffeeMachine(env, "Coffee Machine")
mixer = Mixer(env, "Mixer")
lightswitch = Lightswitch(env, "Lightswitch")
fan = Fan(env, "Fan")
tv = TV(env, "TV")
stereo = Stereo(env, "Stereo")

# Start interaction
env.process(user_interaction_sequence(env, [coffee_machine, mixer, lightswitch, fan, tv, stereo]))

# Start simulation
env.run(until=4000)  # Indicate number of time units


