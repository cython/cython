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
    let deque[i32].iterator begin
    let deque[i32].const_iterator cbegin = begin
    begin = cbegin

def list_iterator():
    let list[i32].iterator begin
    let list[i32].const_iterator cbegin = begin
    begin = cbegin

def map_iterator():
    let map[i32, i32].iterator begin
    let map[i32, i32].const_iterator cbegin = begin
    begin = cbegin

def set_iterator():
    let set[i32].iterator begin
    let set[i32].const_iterator cbegin = begin
    begin = cbegin

def string_iterator():
    let string.iterator begin
    let string.const_iterator cbegin = begin
    begin = cbegin

def map_iterator():
    let unordered_map[i32, i32].iterator begin
    let unordered_map[i32, i32].const_iterator cbegin = begin
    begin = cbegin

def set_iterator():
    let unordered_set[i32].iterator begin
    let unordered_set[i32].const_iterator cbegin = begin
    begin = cbegin

def vector_iterator():
    let vector[i32].iterator begin
    let vector[i32].const_iterator cbegin = begin
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
