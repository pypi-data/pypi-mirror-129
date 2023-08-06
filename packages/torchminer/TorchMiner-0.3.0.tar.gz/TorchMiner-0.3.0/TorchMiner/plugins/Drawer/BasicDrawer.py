# -*- coding:utf-8 -*-
import os

from TorchMiner import BasePlugin


class BasicDrawer(BasePlugin):
    """To visualize everything in training process"""

    def __init__(self, state=None):
        super().__init__()

        if state is None:
            self.state = {}
        else:
            self.state = state

    def prepare(self, miner, *args, **kwargs):
        super(BasicDrawer, self).prepare(miner)
        self.step_file = os.path.join(
            miner.alchemistic_directory, miner.experiment, ".drawer_step"
        )

    def scalars(self, x, value, graph):
        """
        Plot different scalars on a graph
        :param x:
        :param value:
        :param graph:
        :return:
        """
        raise NotImplementedError()

    def scalar(self, x, value, graph):
        """
        Plot one scalar on a graph
        :param x:
        :param value:
        :param graph:
        :return:
        """
        self.scalars(x, {graph: value}, graph)

    def get_state(self):
        """Return current state(counter) of the Drawer"""
        return self.state

    def set_state(self, state):
        """Set current state(counter) to state"""
        self.state = state
