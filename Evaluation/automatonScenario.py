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
        if random.random() < 0.8:
            logger_user.info(f"Switching power on, {env.now}, Coffeemachine")
            logger_machine.info(f"., {env.now}, Coffeemachine")
            CoffeeMachine.power_ison = True
            yield self.env.timeout(1)
            logger_user.info(f"Pressing the button to start Coffeemachine, {env.now}, Coffeemachine")
            logger_machine.info(f"., {env.now}, Coffeemachine")
        else:
            logger_user.info(f"Pressing the button to start Coffeemachine, {env.now}, Coffeemachine")
            logger_machine.info(f"Nothing happens, {env.now}, Coffeemachine")
            yield self.env.timeout(1)
            logger_user.info(f"Switching power on, {env.now}, Coffeemachine")
            logger_machine.info(f"., {env.now}, Coffeemachine")
            yield self.env.timeout(1)
            logger_user.info(f"Pressing the button to start Coffeemachine, {env.now}, Coffeemachine")
            logger_machine.info(f"., {env.now}, Coffeemachine")

        for _ in range(random.randint(1,3)):  # It takes 1 to 3 seconds until the machine starts
            yield self.env.timeout(1)
            logger_machine.info(f"., {env.now}, Coffeemachine")
            logger_user.info(f"., {env.now}, Coffeemachine")  #replace by "Test" to check if the several Input combination works

        yield self.env.timeout(1)
        logger_user.info(f"., {env.now}, Coffeemachine")
        logger_machine.info(f"Starting the brewing, {env.now}, Coffeemachine")

        for _ in range(1):
            yield self.env.timeout(1)

            #if random.random() < 0.002:
            #    logger_user.info(f"Waiting for Coffeemachine, {env.now}, Coffeemachine")
            #    logger_machine.info(f"Stopping, {env.now}, Coffeemachine")
            #    self.interaction_active = False
            #    return
            #elif random.random() < 0.05:
            #    logger_user.info(f"Pressing button to stop, {env.now}, Coffeemachine")
            #    logger_machine.info(f"Stopping, {env.now}, Coffeemachine")
            #    self.interaction_active = False
            #    return
            #else:
            logger_user.info(f"Waiting for Coffeemachine, {env.now}, Coffeemachine")
            logger_machine.info(f"Brewing, {env.now}, Coffeemachine")

        yield self.env.timeout(1)
        logger_machine.info(f"Coffee machine makes a short sound, {env.now}, Coffeemachine")
        logger_user.info(f"Taking the coffee, {env.now}, Coffeemachine")
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Coffeemachine multi-user, {env.now}, Coffeemachine")


class Mixer(Machine):

    overheated = False
    last_used = 0
    used_counter = 0

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
          

        if random.random() < 0.5:
            logger_user.info(f"Pressing the button to start Mixer, {env.now}, Mixer")
            logger_machine.info(f"Nothing happens, {env.now}, Mixer")
            yield self.env.timeout(0)
            self.interaction_active = False
        else:
            logger_user.info(f"Pressing the button to start Mixer, {env.now}, Mixer")
            logger_machine.info(f"Mixer shows a green light, {env.now}, Mixer")
            for _ in range(random.randint(1,2)):  # It takes 1 to 2 seconds until the machine starts
                yield self.env.timeout(1)
                logger_machine.info(f"., {env.now}, Mixer")
                logger_user.info(f"., {env.now}, Mixer")

            yield self.env.timeout(1)
            logger_user.info(f"., {env.now}, Mixer")
            logger_machine.info(f"Starting the mixing, {env.now}, Mixer")
            for _ in range(3):
                yield self.env.timeout(1)
                #if random.random() < 0.01:
                #    logger_machine.info(f"Turning off, {env.now}, Mixer")
                #    logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")
                #    Mixer.overheated = True
                #    Mixer.last_used = env.now
                #    Mixer.used_counter += 1
                #    self.interaction_active = False
                #    return
                #else:
                logger_machine.info(f"Mixing, {env.now}, Mixer")
                logger_user.info(f"Waiting for Mixer, {env.now}, Mixer")

            yield self.env.timeout(1)
            logger_machine.info(f"Mixer stops, {env.now}, Mixer")
            logger_user.info(f"Press button to stop Mixer, {env.now}, Mixer")
            Mixer.overheated = True
            Mixer.last_used = env.now
            Mixer.used_counter += 1
            self.interaction_active = False
            

    def multiuser_operation(self):
        logger_multiuser.info(f"Mixer makes a sound, {env.now}, Mixer")

        
class TV(Machine):

    on = False

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        
        logger_user.info(f"Clap twice, 0, TV")
        logger_machine.info(f"., 0, TV")
        
        for _ in range(random.randint(1,3)):  # It takes 1 to 3 seconds until the TV starts
            yield self.env.timeout(1)
            logger_machine.info(f"., 0, TV")
            logger_user.info(f"., 0, TV")

        yield self.env.timeout(1)
        logger_user.info(f"., 0, TV")
        logger_machine.info(f"TV turns on, 0, TV")
        TV.on = True
        for _ in range(1):
            yield self.env.timeout(1)
            if random.random() < 0.2:
                logger_machine.info(f"TV makes a weird sound, 0, TV")
            else:    
                logger_machine.info(f"TV is on, 0, TV") #Is watching TV
            logger_user.info(f"Watching, 0, TV")

        yield self.env.timeout(1)
        logger_machine.info(f"TV turns off, 0, TV")
        logger_user.info(f"Press power button on the remote, 0, TV")
        TV.on = False
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"TV flickers, {env.now}, TV")

class Stereo(Machine):
    
    on = False

    def __init__(self, env, name):
        super().__init__(env, name)

    def operation(self):
        if Stereo.on:
            logger_user.info(f"Turning Stereo off, {env.now}, Stereo")
            logger_machine.info(f"Stereo turns off, {env.now}, Stereo")
            Stereo.on = False
        else:
            logger_user.info(f"Turning Stereo on, {env.now}, Stereo")
            logger_machine.info(f"Stereo turns on, {env.now}, Stereo")
            Stereo.on = True
        yield self.env.timeout(0)
        self.interaction_active = False


    def multiuser_operation(self):
        logger_multiuser.info(f"Volume of stereo changes, {env.now}, Stereo")


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
    
    def operation(self):
        self.temperature = np.clip(np.random.normal(self.temperature, 0.5), -10, 40)
        if (self.temperature>20 and not self.on):
            logger_machine.info(f"Fan goes on, {env.now}, Fan")
            self.on = True
            logger_user.info(f"Temperature high, {env.now}, Fan")           
        elif (self.temperature<=20 and self.on):
            logger_machine.info(f"Fan goes off, {env.now}, Fan")
            self.on = False
            logger_user.info(f"Temperature low, {env.now}, Fan")
        elif (self.on and random.random() <0.01):
            logger_user.info(f"Fail, {env.now}, Fan") # If we assume that user knows about it 
            logger_machine.info(f"Fan goes ff, {env.now}, Fan")
            self.on = False
            yield env.timeout(1)
            logger_machine.info(f"Fan goes on, {env.now}, Fan")
            self.on = True
            logger_user.info(f"., {env.now}")
        else:
            logger_machine.info(f"., {env.now}")
            logger_user.info(f"., {env.now}")

            
        yield env.timeout(0)
        self.interaction_active = False
        

    def multiuser_operation(self):
        if not self.on:
            logger_multiuser.info(f"Fan goes on, {env.now}, Fan")
            self.on = True
        else:
            logger_multiuser.info(f"., {env.now}")

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

        
        # MULTIUSER
        if random.random() < 0.01:
            inactive_machines = [machine for machine in machines if not machine.interaction_active]
            selected_machine = random.choice(machines)
            selected_machine.multiuser_operation()
        else:
            logger_multiuser.info(f"., {env.now}") 

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
env.process(user_interaction_sequence(env, [tv]))#coffee_machine, mixer, lightswitch, fan, tv, stereo]))

# Start simulation
env.run(until=4000)  # Indicate number of time units


