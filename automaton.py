import simpy
import random
import logging

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
    def __init__(self, env, name):
        super().__init__(env, name)
        self.done = 0
        self.failCount = 0
        self.manualStopCount = 0

    def operation(self):
        logger_machine.info(f"Starting the brewing")
        logger_user.info(f"Pressing the button to start Coffeemachine")

        for _ in range(10):
            yield self.env.timeout(1)

            if random.random() < 0.002:
                logger_user.info(f"Waiting")
                logger_machine.info(f"Stopping")
                self.failCount += 1
                self.interaction_active = False
                return
            elif random.random() < 0.05:
                logger_user.info(f"Pressing button to stop")
                logger_machine.info(f"Stopping")
                self.manualStopCount += 1
                self.interaction_active = False
                return
            else:
                logger_user.info(f"Waiting")
                logger_machine.info(f"Brewing")

        yield self.env.timeout(1)
        logger_machine.info(f"Coffee finished")
        logger_user.info(f"Taking the coffee")
        self.done += 1
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Coffeemachine makes a sound")


class Mixer(Machine):
    def __init__(self, env, name):
        super().__init__(env, name)
        self.mixed = 0

    def operation(self):
        logger_machine.info(f"Starting the mixing")
        logger_user.info(f"Pressing the button to start Mixer")
        for _ in range(3):
            yield self.env.timeout(1)
            if random.random() < 0.01:
                logger_machine.info(f"Turning off")
                logger_user.info(f"Waiting")
                self.interaction_active = False
                return
            else:
                logger_machine.info(f"Mixing")
                logger_user.info(f"Waiting")

        yield self.env.timeout(1)
        logger_machine.info(f"Mixer finished")
        logger_user.info(f"Taking the mixed")
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Mixer makes a sound")

class Lightswitch(Machine):
    def __init__(self, env, name):
        super().__init__(env, name)
        self.lightson = False

    def operation(self):
        if self.lightson:
            logger_user.info(f"Turning lights off")
            logger_machine.info(f"Lights turn off")
            self.lightson = False
        else:
            logger_user.info(f"Turning lights on")
            logger_machine.info(f"Lights turn on")
            self.lightson = True
        yield self.env.timeout(1)
        self.interaction_active = False

    def multiuser_operation(self):
        logger_multiuser.info(f"Light turns red")



def user_interaction_sequence(env, machines):
    while True:
        yield env.timeout(1)

        if not any(machine.interaction_active for machine in machines):
            selected_machine = random.choice(machines)
            if random.random() < 0.5:
                selected_machine.interaction_active = True
                env.process(selected_machine.operation())
            else:
                logger_user.info(f"Doing nothing")
                logger_machine.info(f"Nothing happens")

        if random.random() < 0.01:
            inactive_machines = [machine for machine in machines if not machine.interaction_active]
            selected_machine = random.choice(inactive_machines)
            selected_machine.multiuser_operation()
        else:
            logger_multiuser.info(f"")


# Create environment
env = simpy.Environment()

# Create machines
coffee_machine = CoffeeMachine(env, "Coffee Machine")
mixer = Mixer(env, "Mixer")
lightswitch = Lightswitch(env, "Lightswitch")

# Start interaction
env.process(user_interaction_sequence(env, [coffee_machine, mixer, lightswitch]))

# Start simulation
env.run(until=1600)  # Indicate number of time units

# Print Counts
print("Coffees made:", coffee_machine.done)
print("Fail stops:", coffee_machine.failCount)
print("Manual stops:", coffee_machine.manualStopCount)
