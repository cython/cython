# mode: error
# tag: cpp

from libcpp.deque cimport deque
from libcpp.list cimport list
from libcpp.map cimport map
from libcpp.set cimport set
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.unordered_set cimport unordered_set
from libcpp.vector cimport vector

def deque_iterator():
    cdef deque[i32].iterator begin
    cdef deque[i32].const_iterator cbegin = begin
    begin = cbegin

def list_iterator():
    cdef list[i32].iterator begin
    cdef list[i32].const_iterator cbegin = begin
    begin = cbegin

def map_iterator():
    cdef map[i32, i32].iterator begin
    cdef map[i32, i32].const_iterator cbegin = begin
    begin = cbegin

def set_iterator():
    cdef set[i32].iterator begin
    cdef set[i32].const_iterator cbegin = begin
    begin = cbegin

def string_iterator():
    cdef string.iterator begin
    cdef string.const_iterator cbegin = begin
    begin = cbegin

def map_iterator():
    cdef unordered_map[i32, i32].iterator begin
    cdef unordered_map[i32, i32].const_iterator cbegin = begin
    begin = cbegin

def set_iterator():
    cdef unordered_set[i32].iterator begin
    cdef unordered_set[i32].const_iterator cbegin = begin
    begin = cbegin

def vector_iterator():
    cdef vector[i32].iterator begin
    cdef vector[i32].const_iterator cbegin = begin
    begin = cbegin

_ERRORS = u"""
16:12: Cannot assign type 'const_iterator' to 'iterator'
21:12: Cannot assign type 'const_iterator' to 'iterator'
26:12: Cannot assign type 'const_iterator' to 'iterator'
31:12: Cannot assign type 'const_iterator' to 'iterator'
36:12: Cannot assign type 'const_iterator' to 'iterator'
41:12: Cannot assign type 'const_iterator' to 'iterator'
46:12: Cannot assign type 'const_iterator' to 'iterator'
51:12: Cannot assign type 'const_iterator' to 'iterator'
"""
