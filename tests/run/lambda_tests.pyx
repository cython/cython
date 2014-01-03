# mode: run
# tag: closures, lambda

# Battery of tests for closures in Cython. Based on the collection of
# compiler tests from P423/B629 at Indiana University, Spring 1999 and
# Fall 2000. Special thanks to R. Kent Dybvig, Dan Friedman, Kevin
# Millikin, and everyone else who helped to generate the original
# tests. Converted into a collection of Python/Cython tests by Craig
# Citro.
#
# Note: This set of tests is split (somewhat randomly) into several
# files, simply because putting all the tests in a single file causes
# gcc and g++ to buckle under the load.
#


def g0():
    """
    >>> g0()
    4000
    """
    return (lambda y_1: y_1)(4000)


def g1():
    """
    >>> g1()
    1
    """
    f_3 = (lambda x_2: x_2)
    return (f_3(0)+1)


def g2():
    """
    >>> g2()
    4
    """
    f_5 = (lambda y_4: y_4)
    return f_5(f_5(4))


def g3():
    """
    >>> g3()
    4
    """
    return (lambda f_7: f_7(f_7(4)))((lambda y_6: y_6))


def g5():
    """
    >>> g5()
    9000
    """
    def g4():
      a_8 = 4000
      return lambda b_9: ((a_8)+(b_9))
    return g4()(5000)


def g6():
    """
    >>> g6()
    9000
    """
    return (lambda a_10: (lambda b_11: (a_10)+(b_11)))(4000)(5000)


def g7():
    """
    >>> g7()
    2
    """
    return (lambda f_13: f_13(f_13(0)))((lambda x_12: (x_12+1)))


def g8():
    """
    >>> g8()
    0
    """
    f_16 = (lambda x_15, y_14: x_15)
    a_17 = f_16(0, 1)
    return f_16(a_17, a_17)


def g10():
    """
    >>> g10()
    3
    """
    f_19 = (lambda x_18: x_18)
    def g9():
      a_22 = 0
      b_21 = 1
      c_20 = 2
      return (f_19(a_22))+((f_19(b_21))+(f_19(c_20)))
    return (f_19(0))+(g9())


def g12():
    """
    >>> g12()
    2
    """
    def g11():
      x_23 = 1
      return lambda y_24: ((x_23)+(y_24))
    f_25 = g11()
    x_26 = 0
    return f_25(f_25(x_26))


def g14():
    """
    >>> g14()
    3050
    """
    def g13():
      t_29 = (lambda x_28: (x_28)+(50))
      return lambda f_30: (t_29(f_30(1000)))
    return g13()((lambda y_27: (y_27)+(2000)))


def g15():
    """
    >>> g15()
    3050
    """
    return (lambda t_33: (lambda f_34: t_33(f_34(1000))))((lambda x_32: (x_32)+(50)))((lambda y_31: (y_31)+(2000)))


def g17():
    """
    >>> g17()
    2050
    """
    def g16():
      t_35 = 50
      return lambda f_36: ((t_35)+(f_36()))
    return g16()((lambda : 2000))


def g18():
    """
    >>> g18()
    2050
    """
    return (lambda t_37: (lambda f_38: (t_37)+(f_38())))(50)((lambda : 2000))


def g20():
    """
    >>> g20()
    700
    """
    def g19():
      x_39 = 300
      return lambda y_40: ((x_39)+(y_40))
    return g19()(400)


def g21():
    """
    >>> g21()
    0
    """
    x_44 = 3
    f_43 = (lambda x_42, y_41: x_42)
    if (f_43(0, 0)):
      return f_43(f_43(0, 0), x_44)
    else:
      return 0


def g22():
    """
    >>> g22()
    False
    """
    f_46 = (lambda x_45: (x_45) if (((not ((x_45[0]) == 0))) if (isinstance(x_45, list)) else (False)) else (False))
    return f_46([0,[0,[]]])


def g23():
    """
    >>> g23()
    False
    """
    f_48 = (lambda x_47: (x_47) if (((not ((not ((x_47[0]) == 0))) if (isinstance(x_47, list)) else (False))) if (x_47) else (False)) else (False))
    return f_48(0)


def g24():
    """
    >>> g24()
    []
    """
    f_50 = (lambda x_49: (x_49) if ((True) if (isinstance(x_49, list)) else ((x_49 == []))) else ([]))
    return f_50(0)


def g25():
    """
    >>> g25()
    0
    """
    y_51 = 4
    f_54 = (lambda x_53, y_52: 0)
    return f_54(f_54(y_51, y_51), f_54(y_51, y_51))


def g26():
    """
    >>> g26()
    0
    """
    y_55 = 4
    f_58 = (lambda x_57, y_56: 0)
    return f_58(f_58(y_55, f_58(y_55, y_55)), f_58(y_55, f_58(y_55, y_55)))


def g27():
    """
    >>> g27()
    4
    """
    return (lambda y_59: (lambda f_61: f_61(f_61(y_59)))((lambda y_60: y_60)))(4)


def g28():
    """
    >>> g28()
    23
    """
    f_63 = (lambda x_62: x_62)
    return ((1) if (False) else (f_63(22))+1)


def g29():
    """
    >>> g29()
    5061
    """
    f_68 = (lambda x_65: ((not x_65)) if (x_65) else (x_65))
    f2_67 = (lambda x_64: (10)*(x_64))
    x_66 = 23
    return ((1) if (f_68(x_66 == 0)) else ((x_66)*(f2_67((x_66-1))))+1)


def g30():
    """
    >>> g30()
    1
    """
    one_69 = (lambda n_70: (1) if (n_70 == 0) else (one_69((n_70-1))))
    return one_69(13)


def g31():
    """
    >>> g31()
    True
    """
    even_72 = (lambda x_74: (True) if (x_74 == 0) else (odd_71((x_74-1))))
    odd_71 = (lambda x_73: (False) if (x_73 == 0) else (even_72((x_73-1))))
    return odd_71(13)


def g32():
    """
    >>> g32()
    False
    """
    even_76 = (lambda x_78: (True) if (x_78 == 0) else (odd_75((x_78-1))))
    odd_75 = (lambda x_77: (False) if (x_77 == 0) else (even_76((x_77-1))))
    return even_76(13)


def g34():
    """
    >>> g34()
    True
    """
    even_80 = (lambda x_79: x_79)
    def g33():
      even_82 = (lambda x_84: (True) if (x_84 == 0) else (odd_81((x_84-1))))
      odd_81 = (lambda x_83: (False) if (x_83 == 0) else (even_82((x_83-1))))
      return odd_81(13)
    return even_80(g33())


def g35():
    """
    >>> g35()
    120
    """
    fact_85 = (lambda n_86: (1) if (n_86 == 0) else ((n_86)*(fact_85((n_86-1)))))
    return fact_85(5)


def g38():
    """
    >>> g38()
    10
    """
    x_87 = 5
    a_90 = (lambda u_101, v_100, w_99: (b_89(v_100, w_99)) if (u_101 == 0) else (a_90((u_101)-(1), v_100, w_99)))
    def g37():
      def g36(q_93, r_92):
        p_94 = (q_93)*(r_92)
        e_96 = (lambda n_98: (c_88(p_94)) if (n_98 == 0) else (o_95((n_98)-(1))))
        o_95 = (lambda n_97: (c_88(x_87)) if (n_97 == 0) else (e_96((n_97)-(1))))
        return e_96((q_93)*(r_92))
      return g36
    b_89 = g37()
    c_88 = (lambda x_91: (5)*(x_91))
    return a_90(3, 2, 1)


def g39():
    """
    >>> g39()
    120
    """
    fact_104 = (lambda fact_103, n_102: (1) if (n_102 == 0) else ((fact_103(fact_103, (n_102-1)))*(n_102)))
    return fact_104(fact_104, 5)


def g40():
    """
    >>> g40()
    35
    """
    return (lambda x_105: (lambda y_106: (lambda z_107: (lambda w_108: (lambda u_109: (x_105)+((y_106)+((z_107)+((w_108)+(u_109)))))))))(5)(6)(7)(8)(9)


def g41():
    """
    >>> g41()
    6
    """
    sum_112 = (lambda sum_111, ls_110: (0) if ((ls_110 == [])) else (((ls_110[0]))+(sum_111(sum_111, (ls_110[1])))))
    return sum_112(sum_112, [1,[2,[3,[]]]])


def g46():
    """
    >>> g46()
    1500
    """
    def g45():
      def g44():
        def g42(a_113):
          def g43():
            (a_113)+(200 if True else None)
            return 1500
          return g43
        return g42
      return g44()(1000)
    return g45()()


def g53():
    """
    >>> g53()
    2600
    """
    def g52():
      def g51():
        def g50():
          def g47(a_114):
            def g48(b_115):
              a_114 = 200 if b_115 else None
              def g49(c_116):
                c_116 = 400 if 300 else None
                return (a_114)+((b_115)+(c_116))
              return g49
            return g48
          return g47
        return g50()(1000)
      return g51()(2000)
    return g52()(3000)


def g54():
    """
    >>> g54()
    5
    """
    return (lambda f_118: f_118(f_118(5)))((lambda x_117: x_117))


def g56():
    """
    >>> g56()
    8000
    """
    def g55():
      f_120 = (lambda x_119: (x_119)+(3000))
      return lambda y_121: (f_120(f_120(y_121)))
    return g55()(2000)


def g57():
    """
    >>> g57()
    120
    """
    fact_125 = (lambda fact_124, n_123, acc_122: (acc_122) if (n_123 == 0) else (fact_124(fact_124, (n_123-1), (n_123)*(acc_122))))
    return fact_125(fact_125, 5, 1)


def g58():
    """
    >>> g58()
    3
    """
    f_127 = (lambda x_126: (lambda : x_126()))
    return f_127((lambda : 3))()


def g59():
    """
    >>> g59()
    22
    """
    f_129 = (lambda x_132: (x_132)+((lambda y_133: (lambda z_134: (y_133)+(z_134)))(6)(7)))
    g_128 = (5)+((lambda w_131, u_130: (w_131)+(u_130))(8, 9))
    return g_128


def g60():
    """
    >>> g60()
    0
    """
    loop_135 = (lambda : (lambda : loop_135()))
    loop_135()
    return 0


def g63():
    """
    >>> g63()
    668
    """
    def g62():
      def g61():
        loop_137 = (lambda link_138: (lambda : link_138()))
        return loop_137((lambda : 668))
      return g61
    f_136 = g62()
    return f_136()()


def g64():
    """
    >>> g64()
    17
    """
    k_141 = (lambda x_140, y_139: x_140)
    b_142 = 17
    return k_141(k_141(k_141, 37), 37)(b_142, (b_142)*(b_142))


def g65():
    """
    >>> g65()
    37
    """
    f_145 = (lambda g_144, u_143: g_144((g_144(37)) if (u_143) else (u_143)))
    return f_145((lambda x_146: x_146), 75)


def g66():
    """
    >>> g66()
    4687
    """
    f_150 = (lambda h_148, u_147: h_148((h_148((u_147)+(37))) if (u_147) else (u_147)))
    w_149 = 62
    return f_150((lambda x_151: (w_149)-(x_151)), (75)*(w_149))


def g67():
    """
    >>> g67()
    True
    """
    t_153 = True
    f_152 = False
    bools_156 = [t_153,f_152]
    id_155 = (lambda x_154: (f_152) if ((not x_154)) else (t_153))
    even_158 = (lambda x_160: ((bools_156[0])) if (id_155(x_160 == 0)) else (odd_157((x_160)-(1))))
    odd_157 = (lambda y_159: (id_155((bools_156[1]))) if (y_159 == 0) else (even_158((y_159)-(1))))
    return odd_157(5)


def g68():
    """
    >>> g68()
    5
    """
    f_162 = (lambda x_164: (x_164)+(1))
    g_161 = (lambda y_163: f_162(f_162(y_163)))
    return (f_162(1))+(g_161(1))


def g69():
    """
    >>> g69()
    1521
    """
    y_165 = 3
    f_168 = (lambda x_171: (g_167((x_171)+(1))) if (x_171 == 0) else (f_168((x_171)-(y_165))))
    g_167 = (lambda x_170: h_166((x_170)*(x_170)))
    h_166 = (lambda x_169: x_169)
    return g_167(39)


def g70():
    """
    >>> g70()
    -1
    """
    f_173 = (lambda x_175: (x_175)+(1))
    g_172 = (lambda y_174: f_173(f_173(y_174)))
    f_173 = (lambda x_176: (x_176)-(1))
    return (f_173(1))+(g_172(1))


def g71():
    """
    >>> g71()
    [52, [17, [35, [17, 35]]]]
    """
    f_180 = (lambda : (a_179)+(b_178))
    a_179 = 17
    b_178 = 35
    h_177 = [(lambda : a_179),(lambda : b_178)]
    return [f_180(),[a_179,[b_178,[(h_177[0])(),(h_177[1])()]]]]


def g73():
    """
    >>> g73()
    120
    """
    x_183 = 5
    def g72():
      a_181 = 1
      return lambda : (a_181)
    th_182 = g72()
    fact_184 = (lambda n_186, th_185: (th_185()) if (n_186 == 0) else ((n_186)*(fact_184((n_186)-(1), th_185))))
    return fact_184(x_183, th_182)


def g74():
    """
    >>> g74()
    [120, -120]
    """
    negative_188 = (lambda n_187: (n_187 < 0))
    fact_190 = (lambda n_192: (1) if (n_192 == 0) else ((n_192)*(fact_190((n_192)-(1)))))
    call_fact_189 = (lambda n_191: (fact_190(n_191)) if ((not negative_188(n_191))) else ((0)-(fact_190((0)-(n_191)))))
    return [call_fact_189(5),call_fact_189(-5)]


def g75():
    """
    >>> g75()
    [[33, 55], [77, 99]]
    """
    return (lambda a_193: (lambda b_194: (lambda c_195: (lambda d_196: [[a_193,b_194],[c_195,d_196]]))))(33)(55)(77)(99)

