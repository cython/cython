# mode: run
# tag: closures
# preparse: id
# preparse: def_to_cdef
#
# closure_tests_3.pyx
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


def g1649():
    """
    >>> g1649()
    6
    """
    def g1648():
      def g1647(x_1211):
        return x_1211
      return g1647
    f_1212 = g1648()
    if (f_1212(True)):
      f_1212(3)
      f_1212(4)
    else:
      f_1212(5)
    return f_1212(6)


def g1653():
    """
    >>> g1653()
    5
    """
    def g1652():
      def g1651(x_1213):
        return (x_1213+1)
      return g1651
    f_1214 = g1652()
    def g1650():
      f_1215 = 3
      return (f_1215)+(1)
    return f_1214(g1650())


def g1662():
    """
    >>> g1662()
    51
    """
    x_1223 = 15
    def g1661():
      def g1660(h_1219, v_1218):
        return (h_1219)*(v_1218)
      return g1660
    f_1222 = g1661()
    def g1659():
      def g1658(x_1217):
        return (x_1217)+(5)
      return g1658
    k_1221 = g1659()
    def g1657():
      def g1656(x_1216):
        return (x_1216+1)
      return g1656
    g_1220 = g1657()
    def g1655():
      def g1654():
        g_1224 = 3
        return f_1222(g_1224, x_1223)
      return g_1220(g1654())
    return k_1221(g1655())


def g1665():
    """
    >>> g1665()
    5
    """
    x_1225 = 4
    def g1664():
      def g1663():
        return x_1225
      return g1663
    f_1226 = g1664()
    x_1225 = 5
    return f_1226()


def g1670():
    """
    >>> g1670()
    5
    """
    def g1669():
      def g1668():
        def g1667():
          def g1666():
            return 4
          return g1666
        y_1227 = g1667()
        return y_1227()
      return (g1668()+1)
    x_1228 = g1669()
    return x_1228


def g1674():
    """
    >>> g1674()
    1
    """
    def g1673():
      def g1671(n_1230):
        def g1672():
          return n_1230 == 0
        if (g1672()):
          return 1
        else:
          return one_1229((n_1230-1))
      return g1671
    one_1229 = g1673()
    return one_1229(13)


def g1681():
    """
    >>> g1681()
    True
    """
    def g1680():
      def g1678(x_1234):
        def g1679():
          return x_1234 == 0
        if (g1679()):
          return True
        else:
          return odd_1231((x_1234-1))
      return g1678
    even_1232 = g1680()
    def g1677():
      def g1675(x_1233):
        def g1676():
          return x_1233 == 0
        if (g1676()):
          return False
        else:
          return even_1232((x_1233-1))
      return g1675
    odd_1231 = g1677()
    return odd_1231(13)


def g1688():
    """
    >>> g1688()
    True
    """
    t_1236 = True
    f_1235 = False
    def g1687():
      def g1685(x_1240):
        def g1686():
          return x_1240 == 0
        if (g1686()):
          return t_1236
        else:
          return odd_1237((x_1240-1))
      return g1685
    even_1238 = g1687()
    def g1684():
      def g1682(x_1239):
        def g1683():
          return x_1239 == 0
        if (g1683()):
          return f_1235
        else:
          return even_1238((x_1239-1))
      return g1682
    odd_1237 = g1684()
    return odd_1237(13)


def g1698():
    """
    >>> g1698()
    True
    """
    def g1697():
      def g1696(x_1241):
        return x_1241
      return g1696
    even_1242 = g1697()
    def g1695():
      def g1694():
        def g1692(x_1246):
          def g1693():
            return x_1246 == 0
          if (g1693()):
            return True
          else:
            return odd_1243((x_1246-1))
        return g1692
      even_1244 = g1694()
      def g1691():
        def g1689(x_1245):
          def g1690():
            return x_1245 == 0
          if (g1690()):
            return False
          else:
            return even_1244((x_1245-1))
        return g1689
      odd_1243 = g1691()
      return odd_1243(13)
    return even_1242(g1695())


def g1702():
    """
    >>> g1702()
    120
    """
    def g1701():
      def g1699(n_1248):
        def g1700():
          return n_1248 == 0
        if (g1700()):
          return 1
        else:
          return (n_1248)*(fact_1247((n_1248-1)))
      return g1699
    fact_1247 = g1701()
    return fact_1247(5)


def g1716():
    """
    >>> g1716()
    10
    """
    x_1249 = 5
    def g1715():
      def g1713(u_1263, v_1262, w_1261):
        def g1714():
          return u_1263 == 0
        if (g1714()):
          return b_1251(v_1262, w_1261)
        else:
          return a_1252((u_1263)-(1), v_1262, w_1261)
      return g1713
    a_1252 = g1715()
    def g1712():
      def g1705(q_1255, r_1254):
        p_1256 = (q_1255)*(r_1254)
        def g1711():
          def g1709(n_1260):
            def g1710():
              return n_1260 == 0
            if (g1710()):
              return c_1250(p_1256)
            else:
              return o_1257((n_1260)-(1))
          return g1709
        e_1258 = g1711()
        def g1708():
          def g1706(n_1259):
            def g1707():
              return n_1259 == 0
            if (g1707()):
              return c_1250(x_1249)
            else:
              return e_1258((n_1259)-(1))
          return g1706
        o_1257 = g1708()
        return e_1258((q_1255)*(r_1254))
      return g1705
    b_1251 = g1712()
    def g1704():
      def g1703(x_1253):
        return (5)*(x_1253)
      return g1703
    c_1250 = g1704()
    return a_1252(3, 2, 1)


def g1729():
    """
    >>> g1729()
    537516
    """
    def g1728():
      def g1727(x_1269):
        return (x_1269+1)
      return g1727
    f_1276 = g1728()
    def g1726():
      def g1725(x_1268):
        return (x_1268-1)
      return g1725
    g_1275 = g1726()
    def g1724():
      def g1723(x_1267):
        return (x_1267+1)
      return g1723
    t_1274 = g1724()
    def g1722():
      def g1721(x_1266):
        return (x_1266+1)
      return g1721
    j_1273 = g1722()
    def g1720():
      def g1719(x_1265):
        return (x_1265+1)
      return g1719
    i_1272 = g1720()
    def g1718():
      def g1717(x_1264):
        return (x_1264+1)
      return g1717
    h_1271 = g1718()
    x_1270 = 80
    a_1279 = f_1276(x_1270)
    b_1278 = g_1275(x_1270)
    c_1277 = h_1271(i_1272(j_1273(t_1274(x_1270))))
    return (a_1279)*((b_1278)*((c_1277)+(0)))


def g1733():
    """
    >>> g1733()
    120
    """
    def g1732():
      def g1730(fact_1281, n_1280):
        def g1731():
          return n_1280 == 0
        if (g1731()):
          return 1
        else:
          return (fact_1281(fact_1281, (n_1280-1)))*(n_1280)
      return g1730
    fact_1282 = g1732()
    return fact_1282(fact_1282, 5)


def g1737():
    """
    >>> g1737()
    10000
    """
    def g1736():
      def g1735(x_1283):
        return (x_1283)+(1000)
      return g1735
    f_1284 = g1736()
    def g1734():
      return f_1284(-2) == 0
    if (g1734()):
      return f_1284(6000)
    else:
      return f_1284(f_1284(8000))


def g1741():
    """
    >>> g1741()
    10000
    """
    def g1740():
      def g1739(x_1285):
        return (x_1285)+(1000)
      return g1739
    f_1286 = g1740()
    def g1738():
      return f_1286(-1) == 0
    if (g1738()):
      return f_1286(6000)
    else:
      return f_1286(f_1286(8000))


def g1747():
    """
    >>> g1747()
    8000
    """
    def g1746():
      def g1745(x_1288, y_1287):
        return (x_1288)+(1000)
      return g1745
    f_1289 = g1746()
    def g1744():
      def g1743():
        def g1742():
          return 0
        return f_1289(3000, g1742())
      if (g1743()):
        return f_1289(f_1289(4000, 0), 0)
      else:
        return 8000
    return (g1744())+(2000)


def g1754():
    """
    >>> g1754()
    24
    """
    def g1753():
      def g1752():
        def g1751():
          def g1748(x_1290):
            def g1749(y_1291):
              def g1750(z_1292):
                return (x_1290)+((y_1291)+((z_1292)+(y_1291)))
              return g1750
            return g1749
          return g1748
        return g1751()(5)
      return g1752()(6)
    return g1753()(7)


def g1765():
    """
    >>> g1765()
    35
    """
    def g1764():
      def g1763():
        def g1762():
          def g1761():
            def g1760():
              def g1755(x_1293):
                def g1756(y_1294):
                  def g1757(z_1295):
                    def g1758(w_1296):
                      def g1759(u_1297):
                        return (x_1293)+((y_1294)+((z_1295)+((w_1296)+(u_1297))))
                      return g1759
                    return g1758
                  return g1757
                return g1756
              return g1755
            return g1760()(5)
          return g1761()(6)
        return g1762()(7)
      return g1763()(8)
    return g1764()(9)


def g1769():
    """
    >>> g1769()
    True
    """
    def g1768():
      def g1767(x_1298):
        return x_1298
      return g1767
    f_1299 = g1768()
    def g1766():
      return hasattr(f_1299, '__call__')
    if (g1766()):
      return True
    else:
      return False


def g1779():
    """
    >>> g1779()
    6
    """
    def g1778():
      def g1773(sum_1301, ls_1300):
        def g1777():
          return (ls_1300 == [])
        if (g1777()):
          return 0
        else:
          def g1776():
            return (ls_1300[0])
          def g1775():
            def g1774():
              return (ls_1300[1])
            return sum_1301(sum_1301, g1774())
          return (g1776())+(g1775())
      return g1773
    sum_1302 = g1778()
    def g1772():
      def g1771():
        def g1770():
          return [3,[]]
        return [2,g1770()]
      return [1,g1771()]
    return sum_1302(sum_1302, g1772())


def g1785():
    """
    >>> g1785()
    1500
    """
    def g1784():
      def g1783():
        def g1780(a_1303):
          def g1781():
            def g1782():
              if (True):
                return 200
            (a_1303)+(g1782())
            return 1500
          return g1781
        return g1780
      return g1783()(1000)
    return g1784()()


def g1791():
    """
    >>> g1791()
    102
    """
    def g1790():
      def g1789():
        def g1786(b_1304):
          def g1787(a_1305):
            def g1788():
              if (1):
                return 2
            a_1305 = g1788()
            return (a_1305)+(b_1304)
          return g1787
        return g1786
      return g1789()(100)
    return g1790()(200)


def g1800():
    """
    >>> g1800()
    2600
    """
    def g1799():
      def g1798():
        def g1797():
          def g1792(a_1306):
            def g1793(b_1307):
              def g1794():
                if (b_1307):
                  return 200
              a_1306 = g1794()
              def g1795(c_1308):
                def g1796():
                  if (300):
                    return 400
                c_1308 = g1796()
                return (a_1306)+((b_1307)+(c_1308))
              return g1795
            return g1793
          return g1792
        return g1797()(1000)
      return g1798()(2000)
    return g1799()(3000)


def g1807():
    """
    >>> g1807()
    3628800
    """
    def g1806():
      def g1804(x_1310):
        def g1805():
          return x_1310 == 0
        if (g1805()):
          return 1
        else:
          return (x_1310)*(f_1309((x_1310)-(1)))
      return g1804
    f_1309 = g1806()
    def g1803():
      def g1801(a_1311):
        def g1802(b_1312):
          return a_1311(b_1312)
        return g1802
      return g1801
    g_1313 = g1803()
    return g_1313(f_1309)(10)


def g1828():
    """
    >>> g1828()
    [52, [44, [17, [44, [52, 17]]]]]
    """
    def g1827():
      def g1826():
        return (a_1316)+(b_1315)
      return g1826
    f_1318 = g1827()
    def g1825():
      def g1822(y_1320):
        def g1824():
          def g1823(y_1321):
            return y_1321
          return g1823
        g_1317 = g1824()
        return (y_1320)+(y_1320)
      return g1822
    g_1317 = g1825()
    a_1316 = 17
    b_1315 = 35
    def g1821():
      def g1820():
        def g1819():
          return a_1316
        return g1819
      def g1818():
        def g1817(v_1319):
          a_1316 = v_1319
        return g1817
      return [g1820(),g1818()]
    h_1314 = g1821()
    x1_1324 = f_1318()
    x2_1323 = g_1317(22)
    def g1816():
      def g1815():
        return (h_1314[0])
      return g1815()()
    x3_1322 = g1816()
    x4_1325 = g_1317(22)
    def g1814():
      return (h_1314[1])
    g1814()(3)
    x5_1327 = f_1318()
    def g1813():
      def g1812():
        return (h_1314[0])
      return g1812()()
    x6_1326 = g1813()
    def g1811():
      def g1810():
        def g1809():
          def g1808():
            return [x5_1327,x6_1326]
          return [x4_1325,g1808()]
        return [x3_1322,g1809()]
      return [x2_1323,g1810()]
    return [x1_1324,g1811()]


def g1843():
    """
    >>> g1843()
    [52, [17, [35, [17, 35]]]]
    """
    def g1842():
      def g1841():
        return (a_1330)+(b_1329)
      return g1841
    f_1331 = g1842()
    a_1330 = 17
    b_1329 = 35
    def g1840():
      def g1839():
        def g1838():
          return a_1330
        return g1838
      def g1837():
        def g1836():
          return b_1329
        return g1836
      return [g1839(),g1837()]
    h_1328 = g1840()
    def g1835():
      def g1834():
        def g1833():
          def g1832():
            def g1831():
              return (h_1328[0])
            return g1831()()
          def g1830():
            def g1829():
              return (h_1328[1])
            return g1829()()
          return [g1832(),g1830()]
        return [b_1329,g1833()]
      return [a_1330,g1834()]
    return [f_1331(),g1835()]

