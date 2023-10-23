# mode: compile

fn i32 spam() except 42:
    pass

fn f32 eggs() except 3.14:
    pass

fn char *grail() except NULL:
    pass

fn i32 tomato() except *:
    pass

fn i32 brian() except? 0:
    pass

fn i32 silly() except -1:
    pass

spam()
eggs()
grail()
tomato()
brian()
silly()
