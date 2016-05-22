""" This module collects all loaders. That is, all utils which allow to setup a particular model from an external file.
"""

import xml.etree.ElementTree as ET

import abc
import importlib

from panacea.core.Coordinates import Coordinates2D, Coordinates3D
from panacea.core.Schedule import Schedule


class Loader(object):
    """ Blueprint of the loader object.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def setupFromExternal(self, model):
        """ Sets up from the external file. Note that the path and type of the loader have to be specified
         when instantiating the model.

         Args:
             model (Model): The model instance we are setting up.
        """
        pass

class XMLLoader(Loader):
    """ Loader from our XML format.
    """
    def __init__(self, model):
        """ Constructor method to avoid explicitly having to call setupFromExternal.

         Args:
             model (Model): The model we are setting up.
        """
        xmlPath = model.setupPath
        self.setupFromExternal(xmlPath, model)

    def setupFromExternal(self, xmlPath, model):
        tree = ET.parse(xmlPath)
        root = tree.getroot()

        modelProperties = root.attrib

        # setting epochs
        model.setEpochs(int(modelProperties["epochs"]))

        modelParameters = root.findall("modelParameters/*")

        for m in modelParameters:
            model.addOptionalParameter(m.attrib)

        # grid index, that is all possible types of grids
        gridIndex = root.findall("grids/gridIndex/*")

        # getting all grids which are actually instantiated
        modelGrid = root.findall("grids/modelGrids/*")

        # looping through all grids
        for m in modelGrid:
            # getting the reference to the actual grid class which we will instantiate
            g = filter(lambda x : x.attrib["ref"] == m.attrib["type"], gridIndex)[0].attrib

            # getting parameters for this specific instance
            instanceParameters = m.findall("parameters/*")

            parameters = []

            for p in instanceParameters:
                parameters.append(p.attrib["value"])

            # And finally actually instantiating the class
            module = importlib.import_module(g["module"])
            my_class = getattr(module, g["class"])
            grid = my_class(parameters)

            model.addGrid(grid)

            # NumericalGrid2D objects can have coordinate values
            # defined in xml
            if(g["class"] == "NumericalGrid2D"):
                coordinateValues = m.findall("coordinateValues/*")

                for cv in coordinateValues:
                    cv = cv.attrib

                    grid.setGridValue(Coordinates2D(int(cv["x"]), int(cv["y"])), float(cv["value"]))

        schedule = Schedule()

        # helper index, that is all possible types of helpers
        helperIndex = root.findall("helpers/helperIndex/*")

        # getting all the helpers which are actually instantiated
        modelHelpers = root.findall("helpers/modelHelpers/*")

        #looping through all helpers
        for m in modelHelpers:
            # getting reference to the actual helper class
            h = filter(lambda x : x.attrib["ref"] == m.attrib["type"], helperIndex)[0].attrib

            # getting parameters for this specific instance
            instanceParameters = m.findall("parameters/*")

            parameters = []

            for p in instanceParameters:
                parameters.append(p.attrib["value"])


            # And finally actually instantiating the class
            module = importlib.import_module(h["module"])
            my_class = getattr(module, h["class"])
            helper = my_class(parameters)

            schedule.addHelper(helper)

        # agent index, that is all possible types of agents
        agentIndex = root.findall("agents/agentIndex/*")

        # getting all agents which are actually instantiated
        modelAgents = root.findall("agents/modelAgents/*")

        # looping through agents
        for m in modelAgents:
            # getting reference to the actual agent class
            a = filter(lambda x : x.attrib["ref"] == m.attrib["type"], agentIndex)[0].attrib

            # getting parameters for this specific instance
            instanceParameters = m.findall("parameters/*")

            parameters = []

            for p in instanceParameters:
                parameters.append(p.attrib["value"])


            # And finally actually instantiating the class
            module = importlib.import_module(a["module"])
            my_class = getattr(module, a["class"])
            agent = my_class(parameters)

            schedule.addAgent(agent)

            # Now we have to add the agent to the appropriate grids
            gridPositions = m.findall("gridPositions/*")

            for g in gridPositions:

                # getting the grid
                gridName = g.attrib["grid"]
                grid = model.getGridFromName(gridName)

                # now we get the agent's coordinates for this grid
                coords = g.findall("coordinate")

                # and add them
                if(len(coords) == 2):
                    c = Coordinates2D(int(coords[0].attrib["value"]), int(coords[1].attrib["value"]))
                else:
                    c = Coordinates3D(int(coords[0].attrib["value"]), int(coords[1].attrib["value"]), int(coords[2].attrib["value"]))

                grid.moveAgent(c, agent)

        model.addSchedule(schedule)

