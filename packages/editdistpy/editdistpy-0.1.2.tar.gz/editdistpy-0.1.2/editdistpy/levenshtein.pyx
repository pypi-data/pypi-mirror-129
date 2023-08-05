# distutils: language = c++
# distutils: sources = editdistpy/_levenshtein.cpp
# cython: language_level=3

from libc.stdlib cimport malloc, free

cdef extern from "_levenshtein.hpp":
    ctypedef int int64_t
    int Distance(
        const int* string_1,
        const int* string_2,
        const int string_len_1,
        const int string_len_2,
        const int64_t max_distance,
    )

cpdef int distance(
    object string_1,
    object string_2,
    object max_distance
) except +:
    cdef int len_1 = len(string_1)
    cdef int len_2 = len(string_2)
    cdef int* c_string_1 = <int*>malloc(len_1 * sizeof(int))
    cdef int* c_string_2 = <int*>malloc(len_2 * sizeof(int))
    for i in range(len_1):
        c_string_1[i] = ord(string_1[i])
    for i in range(len_2):
        c_string_2[i] = ord(string_2[i])
    dist = Distance(c_string_1, c_string_2, len_1, len_2, max_distance)
    free(c_string_1)
    free(c_string_2)
    return dist
