# mode: run
# tag: closures
# preparse: id
# preparse: def_to_cdef
#
# closure_tests_1.pyx
#
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

def g1425():
    """
    >>> g1425()
    142
    """
    if (True):
      def g1424():
        if (True):
          return 122
      return (20)+(g1424())
    else:
      return 10000


def g1432():
    """
    >>> g1432()
    [0, []]
    """
    def g1431():
      return [0,[]]
    x_1056 = g1431()
    if (x_1056):
      def g1430():
        def g1429():
          return (x_1056[0])
        def g1428():
          return (x_1056[0])
        return (g1429())+(g1428())
      x_1056[0] = g1430()
    return x_1056


def g1435():
    """
    >>> g1435()
    4000
    """
    def g1434():
      def g1433(y_1057):
        return y_1057
      return g1433
    return g1434()(4000)


def g1438():
    """
    >>> g1438()
    1
    """
    def g1437():
      def g1436(x_1058):
        return x_1058
      return g1436
    f_1059 = g1437()
    return (f_1059(0)+1)


def g1441():
    """
    >>> g1441()
    4
    """
    def g1440():
      def g1439(y_1060):
        return y_1060
      return g1439
    f_1061 = g1440()
    return f_1061(f_1061(4))


def g1446():
    """
    >>> g1446()
    4
    """
    def g1445():
      def g1444(f_1063):
        return f_1063(f_1063(4))
      return g1444
    def g1443():
      def g1442(y_1062):
        return y_1062
      return g1442
    return g1445()(g1443())


def g1449():
    """
    >>> g1449()
    9000
    """
    def g1448():
      a_1064 = 4000
      def g1447(b_1065):
        return (a_1064)+(b_1065)
      return g1447
    return g1448()(5000)


def g1454():
    """
    >>> g1454()
    9000
    """
    def g1453():
      def g1452():
        def g1450(a_1066):
          def g1451(b_1067):
            return (a_1066)+(b_1067)
          return g1451
        return g1450
      return g1452()(4000)
    return g1453()(5000)


def g1459():
    """
    >>> g1459()
    2
    """
    def g1458():
      def g1457(f_1069):
        return f_1069(f_1069(0))
      return g1457
    def g1456():
      def g1455(x_1068):
        return (x_1068+1)
      return g1455
    return g1458()(g1456())


def g1462():
    """
    >>> g1462()
    0
    """
    x_1072 = 0
    def g1461():
      def g1460(x_1070):
        return x_1070
      return g1460
    f_1071 = g1461()
    a_1075 = f_1071(x_1072)
    b_1074 = f_1071(x_1072)
    c_1073 = f_1071(x_1072)
    return ((a_1075)+(b_1074))+(c_1073)


def g1465():
    """
    >>> g1465()
    3
    """
    x_1080 = 0
    y_1079 = 1
    z_1078 = 2
    def g1464():
      def g1463(x_1076):
        return x_1076
      return g1463
    f_1077 = g1464()
    a_1083 = f_1077(x_1080)
    b_1082 = f_1077(y_1079)
    c_1081 = f_1077(z_1078)
    return ((a_1083)+(b_1082))+(c_1081)


def g1468():
    """
    >>> g1468()
    0
    """
    def g1467():
      def g1466(x_1085, y_1084):
        return x_1085
      return g1466
    f_1086 = g1467()
    a_1087 = f_1086(0, 1)
    return f_1086(a_1087, a_1087)


def g1471():
    """
    >>> g1471()
    0
    """
    x_1094 = 0
    y_1093 = 1
    z_1092 = 2
    def g1470():
      def g1469(x_1090, y_1089, z_1088):
        return x_1090
      return g1469
    f_1091 = g1470()
    a_1097 = f_1091(x_1094, y_1093, z_1092)
    b_1096 = y_1093
    c_1095 = z_1092
    return f_1091(a_1097, b_1096, c_1095)


def g1474():
    """
    >>> g1474()
    3
    """
    def g1473():
      def g1472(a_1101, b_1100, c_1099, d_1098):
        return (a_1101)+(d_1098)
      return g1472
    f_1102 = g1473()
    return f_1102(0, 1, 2, 3)


def g1478():
    """
    >>> g1478()
    3
    """
    def g1477():
      def g1476(x_1103):
        return x_1103
      return g1476
    f_1104 = g1477()
    def g1475():
      a_1107 = 0
      b_1106 = 1
      c_1105 = 2
      return (f_1104(a_1107))+((f_1104(b_1106))+(f_1104(c_1105)))
    return (f_1104(0))+(g1475())


def g1483():
    """
    >>> g1483()
    """
    a_1108 = 0
    def g1482():
      def g1481():
        return 0
      return g1481
    a_1110 = g1482()
    def g1480():
      def g1479():
        return 11
      return g1479
    b_1109 = g1480()
    a_1110 = 11


def g1486():
    """
    >>> g1486()
    """
    a_1111 = 0
    def g1485():
      def g1484():
        a_1113 = 0
      return g1484
    a_1113 = g1485()
    b_1112 = 11
    return a_1113()


def g1491():
    """
    >>> g1491()
    0
    """
    def g1490():
      def g1489():
        return 0
      return g1489
    a_1115 = g1490()
    def g1488():
      def g1487():
        return 11
      return g1487
    b_1114 = g1488()
    return a_1115()


def g1494():
    """
    >>> g1494()
    2
    """
    def g1493():
      x_1116 = 1
      def g1492(y_1117):
        return (x_1116)+(y_1117)
      return g1492
    f_1118 = g1493()
    x_1119 = 0
    return f_1118(f_1118(x_1119))


def g1501():
    """
    >>> g1501()
    3050
    """
    def g1500():
      def g1499():
        def g1498(x_1121):
          return (x_1121)+(50)
        return g1498
      t_1122 = g1499()
      def g1497(f_1123):
        return t_1122(f_1123(1000))
      return g1497
    def g1496():
      def g1495(y_1120):
        return (y_1120)+(2000)
      return g1495
    return g1500()(g1496())


def g1508():
    """
    >>> g1508()
    60
    """
    def g1507():
      def g1506():
        def g1505():
          def g1502(a_1124):
            def g1503(b_1125):
              def g1504(c_1126):
                return (a_1124)+((b_1125)+(c_1126))
              return g1504
            return g1503
          return g1502
        return g1505()(10)
      return g1506()(20)
    return g1507()(30)


def g1513():
    """
    >>> g1513()
    5
    """
    def g1512():
      def g1509(b_1127):
        def g1511():
          def g1510(a_1128):
            return (b_1127)+(a_1128)
          return g1510
        return g1511()(2)
      return g1509
    return g1512()(3)


def g1518():
    """
    >>> g1518()
    5
    """
    def g1517():
      def g1516(f_1130):
        return f_1130(f_1130(5))
      return g1516
    def g1515():
      def g1514(x_1129):
        return x_1129
      return g1514
    return g1517()(g1515())


def g1523():
    """
    >>> g1523()
    8000
    """
    def g1522():
      def g1521():
        def g1520(x_1131):
          return (x_1131)+(3000)
        return g1520
      f_1132 = g1521()
      def g1519(y_1133):
        return f_1132(f_1132(y_1133))
      return g1519
    return g1522()(2000)

