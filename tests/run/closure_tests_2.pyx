# mode: run
# tag: closures
# preparse: id
# preparse: def_to_cdef
#
# closure_tests_2.pyx
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


def g1526():
    """
    >>> g1526()
    2
    """
    x_1134 = 0
    def g1525():
      x_1136 = 1
      z_1135 = x_1134
      def g1524(y_1137):
        return (x_1136)+((z_1135)+(y_1137))
      return g1524
    f_1138 = g1525()
    return f_1138(f_1138(x_1134))


def g1535():
    """
    >>> g1535()
    3050
    """
    def g1534():
      def g1533():
        def g1531(t_1141):
          def g1532(f_1142):
            return t_1141(f_1142(1000))
          return g1532
        return g1531
      def g1530():
        def g1529(x_1140):
          return (x_1140)+(50)
        return g1529
      return g1533()(g1530())
    def g1528():
      def g1527(y_1139):
        return (y_1139)+(2000)
      return g1527
    return g1534()(g1528())


def g1540():
    """
    >>> g1540()
    2050
    """
    def g1539():
      t_1143 = 50
      def g1538(f_1144):
        return (t_1143)+(f_1144())
      return g1538
    def g1537():
      def g1536():
        return 2000
      return g1536
    return g1539()(g1537())


def g1547():
    """
    >>> g1547()
    2050
    """
    def g1546():
      def g1545():
        def g1543(t_1145):
          def g1544(f_1146):
            return (t_1145)+(f_1146())
          return g1544
        return g1543
      return g1545()(50)
    def g1542():
      def g1541():
        return 2000
      return g1541
    return g1546()(g1542())


def g1550():
    """
    >>> g1550()
    700
    """
    def g1549():
      x_1147 = 300
      def g1548(y_1148):
        return (x_1147)+(y_1148)
      return g1548
    return g1549()(400)


def g1553():
    """
    >>> g1553()
    0
    """
    x_1152 = 3
    def g1552():
      def g1551(x_1150, y_1149):
        return x_1150
      return g1551
    f_1151 = g1552()
    if (f_1151(0, 0)):
      return f_1151(f_1151(0, 0), x_1152)
    else:
      return 0


def g1562():
    """
    >>> g1562()
    False
    """
    def g1561():
      def g1556(x_1153):
        def g1560():
          def g1559():
            return isinstance(x_1153, list)
          if (g1559()):
            def g1558():
              def g1557():
                return (x_1153[0])
              return (g1557() == 0)
            return (not g1558())
          else:
            return False
        if (g1560()):
          return x_1153
        else:
          return False
      return g1556
    f_1154 = g1561()
    def g1555():
      def g1554():
        return [0,[]]
      return [0,g1554()]
    return f_1154(g1555())


def g1570():
    """
    >>> g1570()
    False
    """
    def g1569():
      def g1563(x_1155):
        def g1568():
          if (x_1155):
            def g1567():
              def g1566():
                return isinstance(x_1155, list)
              if (g1566()):
                def g1565():
                  def g1564():
                    return (x_1155[0])
                  return (g1564() == 0)
                return (not g1565())
              else:
                return False
            return (not g1567())
          else:
            return False
        if (g1568()):
          return x_1155
        else:
          return False
      return g1563
    f_1156 = g1569()
    return f_1156(0)


def g1575():
    """
    >>> g1575()
    []
    """
    def g1574():
      def g1571(x_1157):
        def g1573():
          def g1572():
            return isinstance(x_1157, list)
          if (g1572()):
            return True
          else:
            return (x_1157 == [])
        if (g1573()):
          return x_1157
        else:
          return []
      return g1571
    f_1158 = g1574()
    return f_1158(0)


def g1578():
    """
    >>> g1578()
    4
    """
    y_1159 = 4
    def g1577():
      def g1576(y_1160):
        return y_1160
      return g1576
    f_1161 = g1577()
    return f_1161(f_1161(y_1159))


def g1581():
    """
    >>> g1581()
    0
    """
    y_1162 = 4
    def g1580():
      def g1579(x_1164, y_1163):
        return 0
      return g1579
    f_1165 = g1580()
    return f_1165(f_1165(y_1162, y_1162), f_1165(y_1162, y_1162))


def g1584():
    """
    >>> g1584()
    0
    """
    y_1166 = 4
    def g1583():
      def g1582(x_1168, y_1167):
        return 0
      return g1582
    f_1169 = g1583()
    return f_1169(f_1169(y_1166, y_1166), f_1169(y_1166, f_1169(y_1166, y_1166)))


def g1587():
    """
    >>> g1587()
    0
    """
    y_1170 = 4
    def g1586():
      def g1585(x_1172, y_1171):
        return 0
      return g1585
    f_1173 = g1586()
    return f_1173(f_1173(y_1170, f_1173(y_1170, y_1170)), f_1173(y_1170, f_1173(y_1170, y_1170)))


def g1594():
    """
    >>> g1594()
    4
    """
    def g1593():
      def g1588(y_1174):
        def g1592():
          def g1591(f_1176):
            return f_1176(f_1176(y_1174))
          return g1591
        def g1590():
          def g1589(y_1175):
            return y_1175
          return g1589
        return g1592()(g1590())
      return g1588
    return g1593()(4)


def g1598():
    """
    >>> g1598()
    23
    """
    def g1597():
      def g1596(x_1177):
        return x_1177
      return g1596
    f_1178 = g1597()
    def g1595():
      if (False):
        return 1
      else:
        return f_1178(22)
    return (g1595()+1)


def g1603():
    """
    >>> g1603()
    22
    """
    def g1602():
      def g1601(x_1179):
        return x_1179
      return g1601
    f_1180 = g1602()
    def g1600():
      def g1599():
        return 23 == 0
      return f_1180(g1599())
    if (g1600()):
      return 1
    else:
      return 22


def g1611():
    """
    >>> g1611()
    5061
    """
    def g1610():
      def g1609(x_1182):
        if (x_1182):
          return (not x_1182)
        else:
          return x_1182
      return g1609
    f_1185 = g1610()
    def g1608():
      def g1607(x_1181):
        return (10)*(x_1181)
      return g1607
    f2_1184 = g1608()
    x_1183 = 23
    def g1606():
      def g1605():
        def g1604():
          return x_1183 == 0
        return f_1185(g1604())
      if (g1605()):
        return 1
      else:
        return (x_1183)*(f2_1184((x_1183-1)))
    return (g1606()+1)


def g1614():
    """
    >>> g1614()
    1
    """
    def g1613():
      def g1612():
        return 0
      return g1612
    f_1186 = g1613()
    x_1187 = f_1186()
    return 1


def g1617():
    """
    >>> g1617()
    1
    """
    def g1616():
      def g1615():
        return 0
      return g1615
    f_1188 = g1616()
    f_1188()
    return 1


def g1620():
    """
    >>> g1620()
    4
    """
    def g1619():
      def g1618(x_1189):
        return x_1189
      return g1618
    f_1190 = g1619()
    if (True):
      f_1190(3)
      return 4
    else:
      return 5


def g1623():
    """
    >>> g1623()
    6
    """
    def g1622():
      def g1621(x_1191):
        return x_1191
      return g1621
    f_1192 = g1622()
    (f_1192(4)) if (True) else (5)
    return 6


def g1627():
    """
    >>> g1627()
    120
    """
    def g1626():
      def g1624(fact_1195, n_1194, acc_1193):
        def g1625():
          return n_1194 == 0
        if (g1625()):
          return acc_1193
        else:
          return fact_1195(fact_1195, (n_1194-1), (n_1194)*(acc_1193))
      return g1624
    fact_1196 = g1626()
    return fact_1196(fact_1196, 5, 1)


def g1632():
    """
    >>> g1632()
    144
    """
    def g1631():
      def g1628(b_1199, c_1198, a_1197):
        b_1203 = (b_1199)+(a_1197)
        def g1630():
          def g1629():
            a_1201 = (b_1199)+(b_1199)
            c_1200 = (c_1198)+(c_1198)
            return (a_1201)+(a_1201)
          return (a_1197)+(g1629())
        a_1202 = g1630()
        return (a_1202)*(a_1202)
      return g1628
    return g1631()(2, 3, 4)


def g1639():
    """
    >>> g1639()
    3
    """
    def g1638():
      def g1636(x_1204):
        def g1637():
          return x_1204()
        return g1637
      return g1636
    f_1205 = g1638()
    def g1635():
      def g1634():
        def g1633():
          return 3
        return g1633
      return f_1205(g1634())
    return g1635()()


def g1646():
    """
    >>> g1646()
    3628800
    """
    def g1645():
      def g1643(x_1207):
        def g1644():
          return x_1207 == 0
        if (g1644()):
          return 1
        else:
          return (x_1207)*(f_1206((x_1207)-(1)))
      return g1643
    f_1206 = g1645()
    q_1208 = 17
    def g1642():
      def g1640(a_1209):
        q_1208 = 10
        def g1641():
          return a_1209(q_1208)
        return g1641
      return g1640
    g_1210 = g1642()
    return g_1210(f_1206)()

