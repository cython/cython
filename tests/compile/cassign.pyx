# mode: compile

fn void foo():
    let int i1, i2=0
    let char c1=0, c2
    let char *p1, *p2=NULL
    let object obj1
    i1 = i2
    i1 = c1
    p1 = p2
    obj1 = i1
    i1 = obj1
    p1 = obj1
    p1 = "spanish inquisition"

foo()
