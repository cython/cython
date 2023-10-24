fn i32 spam() except -1:
    raise Exception("Spam error")

fn i32 grail() except -1:
    spam()

def tomato():
    grail()

