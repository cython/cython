# mode: run
# tag: closures
# preparse: id
# preparse: def_to_cdef
#
# closure_tests_4.pyx
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


def g1852():
    """
    >>> g1852()
    [3, 42]
    """
    def g1851():
      def g1850(x_1333):
        x_1334 = 3
        return 3
      return g1850
    f_1332 = g1851()
    def g1848():
      def g1847(x_1336):
        y_1337 = 14
        y_1337 = 7
        return y_1337
      return g1847
    g_1335 = g1848()
    def g1849():
      return [g_1335,3]
    g_1335 = g1849()
    def g1846():
      def g1845(x_1340):
        return x_1340
      return g1845
    h_1339 = g1846()
    z_1338 = 42
    def g1844():
      return (g_1335[1])
    return [g1844(),h_1339(z_1338)]


def g1864():
    """
    >>> g1864()
    True
    """
    t_1342 = True
    f_1341 = False
    def g1863():
      return [t_1342,f_1341]
    bools_1345 = g1863()
    def g1862():
      def g1861(x_1343):
        if ((not x_1343)):
          return f_1341
        else:
          return t_1342
      return g1861
    id_1344 = g1862()
    def g1860():
      def g1857(x_1349):
        def g1859():
          return x_1349 == 0
        if (g1859()):
          def g1858():
            return (bools_1345[0])
          return id_1344(g1858())
        else:
          return odd_1346((x_1349)-(1))
      return g1857
    even_1347 = g1860()
    def g1856():
      def g1853(y_1348):
        def g1855():
          return y_1348 == 0
        if (g1855()):
          def g1854():
            return (bools_1345[1])
          return id_1344(g1854())
        else:
          return even_1347((y_1348)-(1))
      return g1853
    odd_1346 = g1856()
    return odd_1346(5)


def g1872():
    """
    >>> g1872()
    35
    """
    a_1350 = 5
    def g1871():
      return [a_1350,6]
    b_1351 = g1871()
    def g1870():
      def g1869(x_1352):
        return (x_1352)*(a_1350)
      return g1869
    f_1353 = g1870()
    def g1867():
      def g1866():
        return (b_1351[0])
      return (f_1353(a_1350))-(g1866())
    if (g1867()):
      def g1868():
        if ((not a_1350)):
          return (2)*(a_1350)
        else:
          return (2)+(a_1350)
      b_1351[0] = g1868()
      f_1353(a_1350)
    else:
      if ((not (not (f_1353(a_1350) < b_1351)))): (f_1353(a_1350))
    def g1865():
      return (b_1351[0])
    return f_1353(g1865())


def g1885():
    """
    >>> g1885()
    9
    """
    def g1884():
      def g1883(x_1368, y_1367):
        if ((not x_1368)):
          return g_1355((x_1368+1), (y_1367+1))
        else:
          return h_1354((x_1368)+(y_1367))
      return g1883
    f_1356 = g1884()
    def g1882():
      def g1875(u_1359, v_1358):
        a_1361 = (u_1359)+(v_1358)
        b_1360 = (u_1359)*(v_1358)
        def g1881():
          def g1876(d_1363):
            def g1880():
              return [a_1361,b_1360]
            p_1365 = g1880()
            def g1879():
              def g1877(m_1366):
                if ((m_1366 < u_1359)):
                  return f_1356(m_1366, d_1363)
                else:
                  def g1878():
                    return (p_1365[0])
                  return h_1354(g1878())
              return g1877
            q_1364 = g1879()
            return q_1364(f_1356(a_1361, b_1360))
          return g1876
        e_1362 = g1881()
        return e_1362(u_1359)
      return g1875
    g_1355 = g1882()
    def g1874():
      def g1873(w_1357):
        return w_1357
      return g1873
    h_1354 = g1874()
    return f_1356(4, 5)


def g1897():
    """
    >>> g1897()
    22
    """
    def g1896():
      def g1890(x_1373):
        def g1895():
          def g1894():
            def g1893():
              def g1891(y_1374):
                def g1892(z_1375):
                  return (y_1374)+(z_1375)
                return g1892
              return g1891
            return g1893()(6)
          return g1894()(7)
        return (x_1373)+(g1895())
      return g1890
    f_1370 = g1896()
    def g1889():
      def g1888():
        def g1887():
          def g1886(w_1372, u_1371):
            return (w_1372)+(u_1371)
          return g1886
        return g1887()(8, 9)
      return (5)+(g1888())
    g_1369 = g1889()
    return g_1369


def g1923():
    """
    >>> g1923()
    True
    """
    y_1377 = []
    z_1376 = 10
    def g1911():
      return [5,y_1377]
    test_ls_1378 = g1911()
    def g1922():
      def g1913(f_1379):
        def g1921():
          def g1918(g_1382):
            def g1920():
              def g1919(x_1383):
                return g_1382(g_1382)(x_1383)
              return g1919
            return f_1379(g1920())
          return g1918
        def g1917():
          def g1914(g_1380):
            def g1916():
              def g1915(x_1381):
                return g_1380(g_1380)(x_1381)
              return g1915
            return f_1379(g1916())
          return g1914
        return g1921()(g1917())
      return g1913
    y_1377 = g1922()
    def g1912():
      return [z_1376,test_ls_1378]
    test_ls_1378 = g1912()
    def g1910():
      def g1906(ls_1385):
        def g1909():
          return (ls_1385 == [])
        if (g1909()):
          return 0
        else:
          def g1908():
            def g1907():
              return (ls_1385[1])
            return length_1384(g1907())
          return (1)+(g1908())
      return g1906
    length_1384 = g1910()
    len_1386 = length_1384(test_ls_1378)
    def g1905():
      def g1904():
        def g1903():
          def g1898(len_1387):
            def g1899(ls_1388):
              def g1902():
                return (ls_1388 == [])
              if (g1902()):
                return 0
              else:
                def g1901():
                  def g1900():
                    return (ls_1388[1])
                  return len_1387(g1900())
                return (1)+(g1901())
            return g1899
          return g1898
        return y_1377(g1903())
      length_1384 = g1904()
      return length_1384(test_ls_1378)
    return (g1905() == len_1386)


def g1927():
    """
    >>> g1927()
    0
    """
    def g1926():
      def g1924():
        def g1925():
          return loop_1389()
        return g1925
      return g1924
    loop_1389 = g1926()
    loop_1389()
    return 0


def g1935():
    """
    >>> g1935()
    668
    """
    def g1934():
      def g1928():
        def g1933():
          def g1931(link_1392):
            def g1932():
              return link_1392()
            return g1932
          return g1931
        loop_1391 = g1933()
        def g1930():
          def g1929():
            return 668
          return g1929
        return loop_1391(g1930())
      return g1928
    f_1390 = g1934()
    return f_1390()()


def g1946():
    """
    >>> g1946()
    14629
    """
    def g1945():
      def g1944():
        return 1
      return g1944
    if (g1945()):
      a_1393 = 2
      def g1943():
        def g1942():
          def g1941():
            def g1938(x_1394):
              def g1940():
                def g1939():
                  a_1393 = 1
                a_1393 = g1939()
              x_1395 = g1940()
              return x_1395
            return g1938
          return g1941()(1)
        if (g1942()):
          def g1937():
            def g1936():
              return None
            return (a_1393 == g1936())
          if (g1937()):
            return True
          else:
            return False
        else:
          return False
      if (g1943()):
        return 778477
      else:
        return 14629


def g1949():
    """
    >>> g1949()
    2
    """
    def g1948():
      def g1947(x_1396):
        return x_1396
      return g1947
    f_1397 = g1948()
    a_1398 = 1
    return ((f_1397(a_1398))+(a_1398))*(a_1398)


def g1952():
    """
    >>> g1952()
    17
    """
    def g1951():
      def g1950(x_1400, y_1399):
        return x_1400
      return g1950
    k_1401 = g1951()
    b_1402 = 17
    return k_1401(k_1401(k_1401, 37), 37)(b_1402, (b_1402)*(b_1402))


def g1956():
    """
    >>> g1956()
    False
    """
    def g1955():
      def g1953():
        n_1403 = 256
        def g1954():
          return ([0]*n_1403)
        v_1404 = g1954()
        v_1404[32] = n_1403
        return v_1404[32]
      return g1953
    f_1405 = g1955()
    return isinstance(f_1405(), list)


def g1959():
    """
    >>> g1959()
    60
    """
    w_1409 = 4
    x_1408 = 8
    y_1407 = 16
    z_1406 = 32
    def g1958():
      def g1957():
        return (w_1409)+((x_1408)+((y_1407)+(z_1406)))
      return g1957
    f_1410 = g1958()
    return f_1410()


def g1965():
    """
    >>> g1965()
    37
    """
    def g1964():
      def g1962(g_1412, u_1411):
        def g1963():
          if (u_1411):
            return g_1412(37)
          else:
            return u_1411
        return g_1412(g1963())
      return g1962
    f_1413 = g1964()
    def g1961():
      def g1960(x_1414):
        return x_1414
      return g1960
    return f_1413(g1961(), 75)


def g1971():
    """
    >>> g1971()
    4687
    """
    def g1970():
      def g1968(h_1416, u_1415):
        def g1969():
          if (u_1415):
            return h_1416((u_1415)+(37))
          else:
            return u_1415
        return h_1416(g1969())
      return g1968
    f_1418 = g1970()
    w_1417 = 62
    def g1967():
      def g1966(x_1419):
        return (w_1417)-(x_1419)
      return g1966
    return f_1418(g1967(), (75)*(w_1417))


def g1983():
    """
    >>> g1983()
    True
    """
    t_1421 = True
    f_1420 = False
    def g1982():
      return [t_1421,f_1420]
    bools_1424 = g1982()
    def g1981():
      def g1980(x_1422):
        if ((not x_1422)):
          return f_1420
        else:
          return t_1421
      return g1980
    id_1423 = g1981()
    def g1979():
      def g1976(x_1428):
        def g1978():
          def g1977():
            return x_1428 == 0
          return id_1423(g1977())
        if (g1978()):
          return (bools_1424[0])
        else:
          return odd_1425((x_1428)-(1))
      return g1976
    even_1426 = g1979()
    def g1975():
      def g1972(y_1427):
        def g1974():
          return y_1427 == 0
        if (g1974()):
          def g1973():
            return (bools_1424[1])
          return id_1423(g1973())
        else:
          return even_1426((y_1427)-(1))
      return g1972
    odd_1425 = g1975()
    return odd_1425(5)


def g1990():
    """
    >>> g1990()
    48
    """
    def g1989():
      def g1984(x_1431, y_1430, z_1429):
        def g1988():
          def g1987(u_1435, v_1434):
            x_1431 = u_1435
            return (x_1431)+(v_1434)
          return g1987
        f_1437 = g1988()
        def g1986():
          def g1985(r_1433, s_1432):
            y_1430 = (z_1429)+(s_1432)
            return y_1430
          return g1985
        g_1436 = g1986()
        return (f_1437(1, 2))*(g_1436(3, 4))
      return g1984
    return g1989()(10, 11, 12)


def g1997():
    """
    >>> g1997()
    176
    """
    def g1996():
      def g1991(x_1440, y_1439, z_1438):
        f_1444 = False
        def g1995():
          def g1994(r_1442, s_1441):
            y_1439 = (z_1438)+(s_1441)
            return y_1439
          return g1994
        g_1443 = g1995()
        def g1993():
          def g1992(u_1446, v_1445):
            v_1445 = u_1446
            return (x_1440)+(v_1445)
          return g1992
        f_1444 = g1993()
        return (f_1444(1, 2))*(g_1443(3, 4))
      return g1991
    return g1996()(10, 11, 12)


def g2002():
    """
    >>> g2002()
    5
    """
    def g2001():
      def g2000(x_1450):
        return (x_1450)+(1)
      return g2000
    f_1448 = g2001()
    def g1999():
      def g1998(y_1449):
        return f_1448(f_1448(y_1449))
      return g1998
    g_1447 = g1999()
    return (f_1448(1))+(g_1447(1))


def g2010():
    """
    >>> g2010()
    1521
    """
    y_1451 = 3
    def g2009():
      def g2007(x_1457):
        def g2008():
          return x_1457 == 0
        if (g2008()):
          return g_1453((x_1457)+(1))
        else:
          return f_1454((x_1457)-(y_1451))
      return g2007
    f_1454 = g2009()
    def g2006():
      def g2005(x_1456):
        return h_1452((x_1456)*(x_1456))
      return g2005
    g_1453 = g2006()
    def g2004():
      def g2003(x_1455):
        return x_1455
      return g2003
    h_1452 = g2004()
    return g_1453(39)


def g2017():
    """
    >>> g2017()
    -1
    """
    def g2014():
      def g2013(x_1461):
        return (x_1461)+(1)
      return g2013
    f_1459 = g2014()
    def g2012():
      def g2011(y_1460):
        return f_1459(f_1459(y_1460))
      return g2011
    g_1458 = g2012()
    def g2016():
      def g2015(x_1462):
        return (x_1462)-(1)
      return g2015
    f_1459 = g2016()
    return (f_1459(1))+(g_1458(1))


def g2032():
    """
    >>> g2032()
    [52, [17, [35, [17, 35]]]]
    """
    def g2031():
      def g2030():
        return (a_1465)+(b_1464)
      return g2030
    f_1466 = g2031()
    a_1465 = 17
    b_1464 = 35
    def g2029():
      def g2028():
        def g2027():
          return a_1465
        return g2027
      def g2026():
        def g2025():
          return b_1464
        return g2025
      return [g2028(),g2026()]
    h_1463 = g2029()
    def g2024():
      def g2023():
        def g2022():
          def g2021():
            def g2020():
              return (h_1463[0])
            return g2020()()
          def g2019():
            def g2018():
              return (h_1463[1])
            return g2018()()
          return [g2021(),g2019()]
        return [b_1464,g2022()]
      return [a_1465,g2023()]
    return [f_1466(),g2024()]


def g2038():
    """
    >>> g2038()
    120
    """
    x_1469 = 5
    def g2037():
      a_1467 = 1
      def g2036():
        return a_1467
      return g2036
    th_1468 = g2037()
    def g2035():
      def g2033(n_1472, th_1471):
        def g2034():
          return n_1472 == 0
        if (g2034()):
          return th_1471()
        else:
          return (n_1472)*(fact_1470((n_1472)-(1), th_1471))
      return g2033
    fact_1470 = g2035()
    return fact_1470(x_1469, th_1468)


def g2046():
    """
    >>> g2046()
    [120, -120]
    """
    def g2045():
      def g2044(n_1473):
        return (n_1473 < 0)
      return g2044
    negative_1474 = g2045()
    def g2043():
      def g2041(n_1478):
        def g2042():
          return n_1478 == 0
        if (g2042()):
          return 1
        else:
          return (n_1478)*(fact_1476((n_1478)-(1)))
      return g2041
    fact_1476 = g2043()
    def g2040():
      def g2039(n_1477):
        if ((not negative_1474(n_1477))):
          return fact_1476(n_1477)
        else:
          return (0)-(fact_1476((0)-(n_1477)))
      return g2039
    call_fact_1475 = g2040()
    return [call_fact_1475(5),call_fact_1475(-5)]


def g2050():
    """
    >>> g2050()
    [0, 1, 2, 3]
    """
    def g2049():
      def g2048(v_1482, i_1481, n_1480):
        if ((not (i_1481 == n_1480))):
          v_1482[i_1481] = i_1481
          return iota_fill_1479(v_1482, (i_1481)+(1), n_1480)
      return g2048
    iota_fill_1479 = g2049()
    n_1483 = 4
    def g2047():
      return ([0]*n_1483)
    v_1484 = g2047()
    iota_fill_1479(v_1484, 0, n_1483)
    return v_1484


def g2061():
    """
    >>> g2061()
    [[33, 55], [77, 99]]
    """
    def g2060():
      def g2059():
        def g2058():
          def g2057():
            def g2051(a_1485):
              def g2052(b_1486):
                def g2053(c_1487):
                  def g2054(d_1488):
                    def g2056():
                      return [a_1485,b_1486]
                    def g2055():
                      return [c_1487,d_1488]
                    return [g2056(),g2055()]
                  return g2054
                return g2053
              return g2052
            return g2051
          return g2057()(33)
        return g2058()(55)
      return g2059()(77)
    return g2060()(99)


def g2075():
    """
    >>> g2075()
    [[[3, [21, [18, []]]], [4, [28, [24, []]]]], [[[0, [0, [0, []]]], [1, [7, [6, []]]]], [[408, 408], []]]]
    """
    a_1489 = 17
    def g2074():
      def g2064(x_1490):
        x1_1492 = (x_1490)+(1)
        x2_1491 = (x_1490)+(2)
        y1_1494 = (x1_1492)*(7)
        y2_1493 = (x2_1491)*(7)
        z1_1496 = (y1_1494)-(x1_1492)
        z2_1495 = (y2_1493)-(x2_1491)
        w1_1498 = (z1_1496)*(a_1489)
        w2_1497 = (z2_1495)*(a_1489)
        def g2073():
          def g2068(b_1500):
            if ((b_1500 == a_1489)):
              def g2072():
                def g2071():
                  return [z1_1496,[]]
                return [y1_1494,g2071()]
              return [x1_1492,g2072()]
            else:
              def g2070():
                def g2069():
                  return [z2_1495,[]]
                return [y2_1493,g2069()]
              return [x2_1491,g2070()]
          return g2068
        g_1502 = g2073()
        def g2067():
          def g2066(c_1499):
            if ((c_1499 == x_1490)):
              return w1_1498
            else:
              return w2_1497
          return g2066
        h_1501 = g2067()
        def g2065():
          if (((x_1490)*(x_1490) == (x_1490)+(x_1490))):
            return True
          else:
            return (x_1490 < 0)
        if (g2065()):
          return [g_1502(17),g_1502(16)]
        else:
          return [h_1501(x_1490),h_1501((x_1490)-(0))]
      return g2064
    f_1503 = g2074()
    def g2063():
      def g2062():
        return [f_1503(3),[]]
      return [f_1503(-1),g2062()]
    return [f_1503(2),g2063()]

