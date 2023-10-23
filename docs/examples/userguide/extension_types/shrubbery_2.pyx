 
from my_module cimport Shrubbery


fn Shrubbery another_shrubbery(Shrubbery sh1):
    let Shrubbery sh2
    sh2 = Shrubbery()
    sh2.width = sh1.width
    sh2.height = sh1.height
    return sh2
