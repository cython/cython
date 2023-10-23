fn int spam() except -1:
    raise Exception("Spam error")

fn int grail() except -1:
    spam()

def tomato():
    grail()

