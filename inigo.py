from random import expovariate

class Inigo(object):
    """
    A sequence which loses details of information as it grows.
    """

    def __init__(self, halflife, compressor, bound=0):
        self._l = []
        self.halflife = halflife
        self.compressor = compressor
        self.bound = bound

    def __repr__(self):
        return "Inigo(%r)" % self._l

    def __str__(self):
        return "Inigo(%s)" % self._l

    def __len__(self):
        return len(self._l)

    def record(self, item):
        l = self._l

        # Do the actual insertion.
        l.append(item)

        # Get a random possible index.
        i = int(expovariate(1.0 / self.halflife))
        i = len(l) - 1 - i

        if i > 0:
            s = l[i - 1:i + 1]

            # If the slice is compressible, compress it before deletion.
            if len(s) == 2:
                l[i - 1] = self.compressor(*s)
            del l[i]

        # If bounded, perform the bound.
        if self.bound:
            del l[self.bound:]


def newer(old, new):
    return new


def older(old, new):
    return old
