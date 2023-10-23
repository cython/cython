# mode: compile

fn void spam():
    let i128 L
    let u128 U
    let object x = object()
    L = x
    x = L
    U = x
    x = U

spam()
