with_asn = """
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  10.0.0.1 [AS1]  5.372 ms  7.718 ms  10.669 ms
 2  50.131.116.1 [AS7922]  10.973 ms  18.230 ms  17.579 ms
 3  162.151.31.41 [AS7922]  18.173 ms  18.167 ms  18.141 ms
 4  68.85.57.54 [AS7922]  19.826 ms 68.85.154.10 [AS33668]  19.862 ms 68.85.154.34 [AS33668]  19.853 ms
 5  68.86.143.26 [AS33651]  20.079 ms *  20.353 ms
 6  * * *
 7  * 4.69.152.80 [AS3356]  18.052 ms *
 8  72.14.223.91 [AS15169]  19.106 ms  20.031 ms  26.583 ms
 9  64.233.175.235 [AS15169]  26.618 ms 72.14.234.173 [AS15169]  26.599 ms 209.85.253.243 [AS15169]  26.589 ms
10  8.8.8.8 [AS15169]  26.533 ms  26.500 ms  25.964 ms
"""

with_anno_lame = """
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 1700 byte packets
 1  *  0.129 ms !<0-0> *  0.136 ms !<0-0> *  0.134 ms !<0-0>
"""

with_anno_admin_prohib = """
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 1490 byte packets
 1  10.0.0.1 (10.0.0.1)  7.118 ms  5.461 ms  1.845 ms
 2  50.131.116.1 (50.131.116.1)  9.629 ms  9.665 ms  9.742 ms
 3  te-0-7-0-5-sur04.sf19th.ca.sfba.comcast.net (162.151.31.41)  23.091 ms  14.360 ms  10.616 ms
 4  te-1-14-0-4-ar01.oakland.ca.sfba.comcast.net (68.85.57.122)  13.566 ms te-1-14-0-3-ar01.oakland.ca.sfba.comcast.net (68.85.57.54)  15.564 ms te-1-14-0-0-ar01.oakland.ca.sfba.comcast.net (68.85.154.10)  11.706 ms
 5  ae-60-0-ar01.sacramento.ca.ccal.comcast.net (68.86.143.26)  20.080 ms  15.503 ms  13.876 ms
 6  * * *
 7  * * *
 8  10.0.0.1 (10.0.0.1)  1.917 ms !X  1.233 ms !X  1.121 ms !X
"""

with_anno_net_unreach = """
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 1490 byte packets
 1  10.0.0.1 (10.0.0.1)  6.526 ms  6.823 ms  7.203 ms
 2  50.131.116.1 (50.131.116.1)  15.542 ms  21.757 ms  22.595 ms
 3  te-0-7-0-5-sur04.sf19th.ca.sfba.comcast.net (162.151.31.41)  23.833 ms  24.798 ms  25.113 ms
 4  te-1-14-0-1-ar01.oakland.ca.sfba.comcast.net (68.85.154.34)  28.144 ms te-1-14-0-3-ar01.oakland.ca.sfba.comcast.net (68.85.57.54)  28.706 ms  29.025 ms
 5  ae-60-0-ar01.sacramento.ca.ccal.comcast.net (68.86.143.26)  26.675 ms  27.853 ms  28.308 ms
 6  * * *
 7  ae-3-80.edge1.sanjose3.level3.net (4.69.152.144)  21.620 ms  20.213 ms  20.653 ms
 8  10.0.0.1 (10.0.0.1)  1.580 ms !N  6.326 ms !N  6.787 ms !N
"""

with_anno_AS = """
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 1490 byte packets
 1  10.0.0.1 (10.0.0.1) [AS1]  3.545 ms  3.830 ms  4.302 ms
 2  50.131.116.1 (50.131.116.1) [AS7922]  17.392 ms  19.454 ms  22.219 ms
 3  te-0-7-0-5-sur04.sf19th.ca.sfba.comcast.net (162.151.31.41) [AS7922]  22.237 ms  23.350 ms  23.368 ms
 4  te-1-14-0-0-ar01.oakland.ca.sfba.comcast.net (68.85.154.10) [AS33668]  23.369 ms te-1-14-0-2-ar01.oakland.ca.sfba.comcast.net (68.87.226.86) [AS33651]  23.370 ms  23.371 ms
 5  ae-60-0-ar01.sacramento.ca.ccal.comcast.net (68.86.143.26) [AS33651]  23.632 ms  23.880 ms  23.897 ms
 6  * * *
 7  ae-3-80.edge1.sanjose3.level3.net (4.69.152.144) [AS3356]  24.064 ms * *
 8  10.0.0.1 (10.0.0.1) [AS1]  1.710 ms !N  2.025 ms !N  2.506 ms !N
"""

