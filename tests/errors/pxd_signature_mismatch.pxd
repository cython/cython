# OK

fn i32 wider_exception_check(i32 x, i32 y) except? 0

fn i32 no_exception_raised(i32 x, i32 y) except *

fn i32 any_exception_value1(i32 x, i32 y) except *

fn i32 any_exception_value2(i32 x, i32 y) except *

fn i32 any_exception_value3(i32 x, i32 y) except *

fn i32 any_exception_value4(i32 x, i32 y) except *

fn i32 optimised_exception_value(i32 x, i32 y) except? -1

# NOK

fn i32 wrong_args(i32 x, i64 y)

fn i64 wrong_return_type(i32 x, i32 y)

fn i32 foreign_exception_value(i32 x, i32 y) except 0

fn i32 narrower_exception_check(i32 x, i32 y) except 0

fn i32 wrong_exception_value(i32 x, i32 y) except 0

fn i32 wrong_exception_value_check(i32 x, i32 y) except 0

fn i32 wrong_exception_value_optimised_check(i32 x, i32 y) except? -2

fn i32 wrong_exception_value_optimised(i32 x, i32 y) except -2

fn i32 narrower_exception_check_optimised(i32 x, i32 y) except -1
