import random
import time

EXHIBITORY = 20  # divides incoming voltage by value: incoming voltage 100 --> results in 5mv change in result
INHIBITORY = -20
ELECTRICAL = 1

STEP_TIME = 1  # waiting time between steps in seconds


class Neuron:
    def __init__(self, action_potential=None, trigger=None):
        self.charge = -70.0  # initialize to resting potential
        self.children = []
        self.action_potential = random.randint(100, 130) if action_potential is None else action_potential
        self.trigger_voltage = random.randint(-65, -55) if trigger is None else trigger

    def __str__(self):
        children = ""
        for child in self.children:
            children += str(child) + ",\n"
        return (f"Neuron:\n"
                f"   AP:{self.action_potential}\n"
                f"   TV:{self.trigger_voltage}\n"
                f"   CH:{self.charge}\n"
                f"   Children:[\n{children}]")

    def add_child(self, synapse):
        self.children.append(synapse)

    def influence_charge(self, difference):
        self.charge += difference
        self.update()

    def neutralize(self):
        self.charge -= (self.charge + 70.0) * 0.15

    def trigger(self):
        self.charge = self.action_potential
        for synapse in self.children:
            synapse.trigger(self.charge)

    def update(self):
        time.sleep(1)
        if self.charge >= self.trigger_voltage:
            self.trigger()

        self.neutralize()

    def set_charge(self, charge):
        self.charge = charge


class Synapse:
    def __init__(self, synapse_type):
        self.type = synapse_type
        self.child = None

    def __str__(self):
        return (f"Synapse:\n"
                f"   Type:{self.type}\n"
                f"   Child:[\n{self.child}]")

    def set_child(self, neuron: Neuron):
        self.child = neuron

    def trigger(self, charge):  # takes an incoming charge and influences downstream neuron based on type of synapse
        if self.child:
            self.child.influence_charge(charge / self.type)


if __name__ == '__main__':
    # create first neuron
    starting_neuron = Neuron()
    synapse_to_second = Synapse(EXHIBITORY)
    starting_neuron.add_child(synapse_to_second)
    synapse_to_third = Synapse(INHIBITORY)
    starting_neuron.add_child(synapse_to_third)

    # create second neuron
    second_neuron = Neuron()
    synapse_to_second.set_child(second_neuron)

    # create third neuron
    third_neuron = Neuron()
    synapse_to_third.set_child(third_neuron)

    print(starting_neuron)