from random import expovariate

class Inigo(object):
    """
    A sequence which loses details of information as it grows.

    Inigos are append-only sequences. When they grow, they occasionally
    discard data, so that they tend towards a logarithmic bound on their size,
    rather than the standard linear bound.

    The half-life of an inigo is the average time taken to discard half of the
    information recorded on the inigo.

    The compressor is a function which takes two items in an inigo and returns
    a single item which summarizes the two inputs. Compressors can choose one
    of the two inputs to return, or create new items for the inigo to
    remember.

    The bound is an optional integer which limits the total size of the inigo.
    If the inigo is bounded, it will never grow beyond the bound; data which
    would exceed the bound will be discarded when new data is recorded.

    The size complexity of an inigo is linear for all operations, and
    recording data in an inigo is linear in time in the worst case.
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

    def __getitem__(self, index):
        return self._l[index]

    def __iter__(self):
        return iter(self._l)

    def aslist(self):
        """
        Convert an inigo to a list.

        The resulting list is safe to mutate without disturbing the inigo that
        it comes from.
        """

        return self._l[:]

    def record(self, item):
        """
        Remember an item for an indeterminate amount of time.
        """

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
    """
    Compress, preferring the newer of the two items.
    """

    return new


def older(old, new):
    """
    Compress, preferring the older of the two items.
    """

    return old
