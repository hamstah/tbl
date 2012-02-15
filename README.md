See data.tbl for examples of formats

Examples of usage

```
$ ./tbl.py data.tbl 

Sort

+------------+--------------+----------+
|       Blah |         Test |       Rr |
+------------+--------------+----------+
|        aaa |            0 |      222 |
|        bbb |            0 |      111 |
|        bbb |            0 |      222 | stays attached to the right row
+------------+--------------+----------+
|        aaa |          111 |      999 |
|        ccc |          222 |      333 |
|        aaa |          333 |        0 |
+------------+--------------+----------+


Missing column text

+-------+-------+---+
| Test1 | Test2 |   |
+-------+-------+---+
|     a |     b | c |
|     d |     e | f |
+-------+-------+---+


Matrix

+---+---+---+
| a | b | c |
+---+---+---+
| d | e | f |
+---+---+---+
| g | h | i |
+---+---+---+


Empty

+---+---+---+
| a | b | c |
| d | e | f |
| g | h | i |
+---+---+---+


Clean build

+--------------+-----------+-------+---------+---------+-----+-------+------+
| Build System |  Compiler | Cache | Threads | Linking | Pch |  Time | Size |
+--------------+-----------+-------+---------+---------+-----+-------+------+
|        Ninja |   gcc 4.4 |  Cold |      12 |  static |  no | 05:07 | 4.7G |
|        Ninja |   gcc 4.4 | 1 run |      12 |  static |  no | 05:00 | 4.7G | **
|         Make |   gcc 4.4 |  Cold |      12 |  static |  no | 05:20 | 4.8G |
|         Make |   gcc 4.4 | 1 run |      12 |  static |  no | 05:07 | 4.8G |
+--------------+-----------+-------+---------+---------+-----+-------+------+
|        Ninja |   gcc 4.4 |  Cold |      12 |  shared |  no | 05:03 | 3.7G |
|        Ninja |   gcc 4.4 | 1 run |      12 |  shared |  no | 04:53 | 3.7G | ** best overall
|         Make |   gcc 4.4 |  Cold |      12 |  shared |  no | 05:11 | 3.8G |
|         Make |   gcc 4.4 | 1 run |      12 |  shared |  no | 05:02 | 3.8G |
+--------------+-----------+-------+---------+---------+-----+-------+------+
|        Ninja | clang 3.1 |  Cold |      12 |  static |  no | xx:xx | x.xG |
|        Ninja | clang 3.1 | 1 run |      12 |  static |  no | xx:xx | x.xG |
|         Make | clang 3.1 |  Cold |      12 |  static |  no | xx:xx | x.xG |
|         Make | clang 3.1 | 1 run |      12 |  static |  no | xx:xx | x.xG |
+--------------+-----------+-------+---------+---------+-----+-------+------+
|        Ninja | clang 3.1 |  Cold |      12 |  shared |  no | xx:xx | x.xG |
|        Ninja | clang 3.1 | 1 run |      12 |  shared |  no | xx:xx | x.xG |
|         Make | clang 3.1 |  Cold |      12 |  shared |  no | xx:xx | x.xG |
|         Make | clang 3.1 | 1 run |      12 |  shared |  no | xx:xx | x.xG |
+--------------+-----------+-------+---------+---------+-----+-------+------+


Incremental

+--------------+----------+---------+---------+-----+-------+--------+
| Build System | Compiler | Threads | Linking | Pch |  Time | Target |
+--------------+----------+---------+---------+-----+-------+--------+
|        Ninja |  gcc 4.4 |      12 |  static |  no | 00:42 |    all | **
|         Make |  gcc 4.4 |      12 |  static |  no | 00:44 |    all |
+--------------+----------+---------+---------+-----+-------+--------+
|        Ninja |  gcc 4.4 |      12 |  static |  no | 00:12 | client | **
|         Make |  gcc 4.4 |      12 |  static |  no | 00:09 | client |
+--------------+----------+---------+---------+-----+-------+--------+
```

Passwd file

```
$ echo "Login, passwd, uid, gid, info, home, shell" | cat - /etc/passwd | sed -e 's/:/,/g' | ./tbl.py 
+-------------+--------+-------+-------+------------------------------------+------------------+-------------------+--+-----------------------+------------+
|       Login | Passwd |   Uid |   Gid |                               Info |             Home |             Shell |  |                       |            |
+-------------+--------+-------+-------+------------------------------------+------------------+-------------------+--+-----------------------+------------+
|        root |      x |     0 |     0 |                               root |            /root |         /bin/bash |  |                       |            |
|      daemon |      x |     1 |     1 |                             daemon |        /usr/sbin |           /bin/sh |  |                       |            |
|         bin |      x |     2 |     2 |                                bin |             /bin |           /bin/sh |  |                       |            |
|         sys |      x |     3 |     3 |                                sys |             /dev |           /bin/sh |  |                       |            |
+-------------+--------+-------+-------+------------------------------------+------------------+-------------------+--+-----------------------+------------+
```