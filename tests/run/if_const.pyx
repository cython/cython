
cimport cython

DEF INT_VAL = 1

def int_bool_result():
    """
    >>> int_bool_result()
    True
    """
    if 5:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_true():
    """
    >>> if_compare_true()
    True
    """
    if 0 == 0:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_false():
    """
    >>> if_compare_false()
    False
    """
    if 0 == 1:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_or_true():
    """
    >>> if_compare_or_true()
    True
    """
    if 0 == 1 or 1 == 1:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_or_false():
    """
    >>> if_compare_or_false()
    False
    """
    if 0 == 1 or 1 == 0:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_and_true():
    """
    >>> if_compare_and_true()
    True
    """
    if 0 == 0 and 1 == 1:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_and_false():
    """
    >>> if_compare_and_false()
    False
    """
    if 1 == 1 and 1 == 0:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def if_compare_cascaded():
    """
    >>> if_compare_cascaded()
    True
    """
    if 0 < 1 < 2 < 3:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//CoerceToBooleanNode",
                                 "//ListNode",
                                 "//IfStatNode")
def list_bool_result_true():
    """
    >>> list_bool_result_true()
    True
    """
    if [1,2,3]:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//CoerceToBooleanNode",
                                 "//ListNode",
                                 "//IfStatNode")
def list_bool_result_false():
    """
    >>> list_bool_result_false()
    False
    """
    if []:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//PrimaryCmpNode",
                                 "//IfStatNode")
def compile_time_DEF_if():
    """
    >>> compile_time_DEF_if()
    True
    """
    if INT_VAL != 0:
        return True
    else:
        return False
