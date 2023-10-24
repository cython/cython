import math

def great_circle(f64 lon1, f64 lat1, f64 lon2, f64 lat2):
    let f64 radius = 3956  # miles
    let f64 x = math.pi/180.0
    let f64 a, b, theta, c

    a = (90.0 - lat1)  *x
    b = (90.0 - lat2) * x
    theta = (lon2 - lon1) * x
    c = math.acos(math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b) * math.cos(theta))

    return radius * c
