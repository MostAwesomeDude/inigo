import random


class Inigo(object):
    """
    A sequence which loses details of information as it grows.

    Inigos are append-only sequences. When they grow, they occasionally
    discard data, so that they tend towards a logarithmic bound on their size,
    rather than the standard linear bound.

    The size complexity of an inigo is linear for all operations, and
    recording data in an inigo is linear in time in the worst case.

    The half-life of an inigo is the average time taken to discard half of the
    information recorded on the inigo.

    The compressor is a function which takes two items in an inigo and returns
    a single item which summarizes the two inputs. Compressors can choose one
    of the two inputs to return, or create new items for the inigo to
    remember.

    The bound is an optional integer which limits the total size of the inigo.
    If the inigo is bounded, it will never grow beyond the bound; data which
    would exceed the bound will be discarded when new data is recorded.

    The ``r`` parameter is an optional callable which yields random indices
    into the list. It can be used to alter inigo behavior, or more usefully to
    make inigo data loss predictable. It defaults to ``random.expovariate``
    and should generally be a stream of exponentially-distributed integers.
    """

    def __init__(self, halflife, compressor, bound=0, r=None):
        self._l = []
        self.halflife = halflife
        self.compressor = compressor
        self.bound = bound

        if r is None:
            self.r = random.expovariate
        else:
            self.r = r

    def __repr__(self):
        return "Inigo(%r)" % self._l

    def __str__(self):
        return "Inigo(%s)" % self._l

    def __eq__(self, other):
        return list(self) == list(other)

    def __len__(self):
        return len(self._l)

    def __getitem__(self, index):
        return self._l[index]

    def __iter__(self):
        return iter(self._l)

    def record(self, item):
        """
        Remember an item for an indeterminate amount of time.
        """

        l = self._l

        # Do the actual insertion.
        l.append(item)

        # Get a random possible index.
        i = int(self.r(1.0 / self.halflife))
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


from unittest import TestCase


class TestInigo(TestCase):

    def test_bound(self):
        i = Inigo(2, older, bound=10)
        # Over-saturate. 2**10 is 1024, so 2000 items of history should
        # overfill the inigo.
        for x in range(2000):
            i.record(x)
        self.assertEqual(len(i), 10)

    def test_repeatability(self):
        r1 = random.Random(42).expovariate
        i1 = Inigo(2, older, bound=10, r=r1)
        r2 = random.Random(42).expovariate
        i2 = Inigo(2, older, bound=10, r=r2)

        for x in range(5000):
            i1.record(x)
            i2.record(x)

        self.assertEqual(i1, i2)
