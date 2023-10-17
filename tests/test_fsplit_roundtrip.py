# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

# import ttcal.day
# import typing
# from hypothesis import given, strategies as st


# @st.composite
# def str_and_ndexes(draw):
#     strval = draw(st.text())
#     ndexes = draw(st.lists(st.integers(min_value=0, max_value=len(strval))))
#     return strval, tuple(sorted(set(ndexes)))


# @given(strndx = str_and_ndexes())
# def test_roundtrip_fsplit_fjoin(strndx):
#     strval, ndexes = strndx
#     value0 = ttcal.day.fsplit(strval, *ndexes)
#     value1 = ttcal.day.fjoin(value0, *ndexes)
#     print("LOCALS:", locals())
#     assert strval == value1, (strval, value1)
