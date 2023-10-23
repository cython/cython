# OK

fn int wider_exception_check(int x, int y) except? 0

fn int no_exception_raised(int x, int y) except *

fn int any_exception_value1(int x, int y) except *

fn int any_exception_value2(int x, int y) except *

fn int any_exception_value3(int x, int y) except *

fn int any_exception_value4(int x, int y) except *

fn int optimised_exception_value(int x, int y) except? -1

# NOK

fn int wrong_args(int x, long y)

fn long wrong_return_type(int x, int y)

fn int foreign_exception_value(int x, int y) except 0

fn int narrower_exception_check(int x, int y) except 0

fn int wrong_exception_value(int x, int y) except 0

fn int wrong_exception_value_check(int x, int y) except 0

fn int wrong_exception_value_optimised_check(int x, int y) except? -2

fn int wrong_exception_value_optimised(int x, int y) except -2

fn int narrower_exception_check_optimised(int x, int y) except -1
