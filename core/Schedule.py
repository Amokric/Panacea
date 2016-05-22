"""The schedule is responsible for holding all steppables (agents and helpers) and progressing the evolution
of the model by calling their respective "step" methods.

.. moduleauthor:: Dario Panada <dario.panada@postgrad.manchester.ac.uk>
"""
from random import shuffle

class Schedule(object):
    """ The main schedule class.
    """

    def __init__(self):
        """ Constructor, initiates the agents and helpers lists to empty.
        """
        self.agents = []
        self.helpers = []

    def addAgent(self, agent):
        """ Adds an agent to the schedule.

        Args:
            agent (agent): The agent we want to add.
        """
        self.agents.append(agent)

    def addHelper(self, helper):
        """ Adds an helper to the schedule.

        Args:
            helper (helper): The helper we want to add.
        """
        self.helpers.append(helper)

    def removeAgent(self, agent):
        """ Removes an agent from the schedule.

        Args:
            agent (agent): The agent we want to remove.
        """
        self.agents.remove(agent)

    def removeHelper(self, helper):
        """ Removes an helper from the schedule.

        Args:
            helper (helper): The helper we want to remove.
        """
        self.helpers.remove(helper)

    def step(self, model):
        """ Steps all agents and helpers. Agents are stepped in a different order at each time-step, hence why
         the list is shuffled. As panacea implements a three-act time-step, steppables see their methods stepPrologue,
         stepMain and stepEpilogue called in that order. In each act, helpers are always stepped before agents.

         Args:
             model (model): The current model, this is then passed to agents and steppables so that they can "see"
             the world they live in and interact with it.
        """
        shuffle(self.agents)

        self.stepPrologue(model)
        self.stepMain(model)
        self.stepEpilogue(model)

    def stepPrologue(self, model):
        """ Calls the stepPrologue method in all helpers and then agents, passing the state of the model to each.

        Args:
            model (model): The current model object.
        """
        for h in self.helpers:
            h.stepPrologue(model)

        for a in self.agents:
            a.stepPrologue(model)

    def stepMain(self, model):
        """ Calls the stepMain method in all helpers and then agents, passing the state of the model to each.

        Args:
            model (model): The current model object.
        """
        for h in self.helpers:
            h.stepMain(model)

        for a in self.agents:
            a.stepMain(model)

    def stepEpilogue(self, model):
        """ Calls the steEpilogue method in all helpers and then agents, passing the state of the model to each.

        Args:
            model (model): The current model object.
        """
        for h in self.helpers:
            h.stepEpilogue(model)

        for a in self.agents:
            a.stepEpilogue(model)
