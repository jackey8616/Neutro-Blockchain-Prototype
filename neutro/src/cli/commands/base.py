"""This class is the parent for all commands of the clinet"""


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError(
            'You must implement the run() method yourself!')
