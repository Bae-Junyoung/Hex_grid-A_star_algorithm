import collections

_Hex = collections.namedtuple("Hex", ["q", "r", "s"])


def Hex(q, r, s):
    assert not (round(q + r + s) != 0), "q + r + s must be 0"
    return _Hex(q, r, s)


EVEN = 1
ODD = -1


def qoffset_to_cube(offset, h):
    q = h.q
    r = h.r - (h.q + offset * (h.q & 1)) // 2
    s = -q - r
    if offset != EVEN and offset != ODD:
        raise ValueError("offset must be EVEN (+1) or ODD (-1)")
    return Hex(q, r, s)


def hex_subtract(a, b):
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)


def hex_length(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hex_distance(a, b):
    return hex_length(hex_subtract(a, b))