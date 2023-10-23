# mode: compile

extern from "string.h":
    void memcpy(void* des, void* src, i32 size)

fn void f():
    let f32[3] f1
    let f32* f2
    f2 = f1 + 1
    memcpy(f1, f2, 1)

f()
