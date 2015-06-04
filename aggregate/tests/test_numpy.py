import itertools
import pytest
import numpy as np

from ..aggregate_numpy import aggregate

@pytest.mark.parametrize("first_last", ["first", "last"])
def test_first_last(first_last):
    group_idx = np.arange(0, 100, 2, dtype=int).repeat(5)
    a = np.arange(group_idx.size)
    res = aggregate(group_idx, a, func=first_last, fill_value=-1)
    ref = np.zeros(np.max(group_idx) + 1)
    ref.fill(-1)
    ref[::2] = np.arange(0 if first_last == 'first' else 4, group_idx.size, 5, dtype=int)
    np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize(["first_last", "nanoffset"], itertools.product(["nanfirst", "nanlast"], [2, 0, 4]))
def test_nan_first_last(first_last, nanoffset):
    group_idx = np.arange(0, 100, 2, dtype=int).repeat(5)
    a = np.arange(group_idx.size, dtype=float)

    a[nanoffset::5] = np.nan
    res = aggregate(group_idx, a, func=first_last, fill_value=-1)
    ref = np.zeros(np.max(group_idx) + 1)
    ref.fill(-1)

    if first_last == "nanfirst":
        ref_offset = 1 if nanoffset == 0 else 0
    else:
        ref_offset = 3 if nanoffset == 4 else 4
    ref[::2] = np.arange(ref_offset, group_idx.size, 5, dtype=int)
    np.testing.assert_array_equal(res, ref)

