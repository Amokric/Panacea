import unittest

from panacea.MResModel.TumourAgents import *


class TestSteppables(unittest.TestCase):

    def test_healthy_cell_setup(self):
        hc = HealthyCell()
        self.assertEqual([],hc.oxygen_thresholds)

if __name__ == '__main__':
    unittest.main()