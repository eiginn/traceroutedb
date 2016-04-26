===============================
TracerouteDB
===============================

.. image:: https://scrutinizer-ci.com/g/eiginn/traceroutedb/badges/quality-score.png?b=master
        :target: https://scrutinizer-ci.com/g/eiginn/traceroutedb/?branch=master

.. image:: https://img.shields.io/pypi/v/traceroutedb.svg
        :target: https://pypi.python.org/pypi/traceroutedb

.. image:: https://readthedocs.org/projects/traceroutedb/badge/?version=latest
        :target: https://readthedocs.org/projects/traceroutedb/?badge=latest
        :alt: Documentation Status


Experiment in full mesh historical traceroutes

Lasciate ogne speranza, voi ch'intrate.

This is an UNFINISHED project and likely won't even work depending on what bad changes have been made at any one time.

* Free software: GPLv2 license
* Documentation: https://traceroutedb.readthedocs.org.

Features
--------

* TODO


Examples
--------

find traceroutes where any hop is over a time
    .. code-block:: sql

        dev_fzt> SELECT * FROM traceroute WHERE traceroute_id in (SELECT DISTINCT traceroute_id FROM hop where (hop_kvs->'time')::float > 10);
        +-----------------+-------------+---------------+----------------------------------+------------+
        |   traceroute_id | origin_ip   | dest_ip       | cdate                            | reporter   |
        |-----------------+-------------+---------------+----------------------------------+------------|
        |               6 | 10.0.0.43   | 173.245.48.10 | 2015-02-02 22:15:17.632821-08:00 | nm         |
        |               7 | 10.0.0.43   | 8.8.8.8       | 2015-02-02 22:52:46.240210-08:00 | nm         |
        +-----------------+-------------+---------------+----------------------------------+------------+

find full traceroute like output
    .. code-block:: sql

        dev_fzt> SELECT t.reporter, t.origin_ip, t.dest_ip, hop.* from traceroute as t INNER JOIN hop USING (traceroute_id) WHERE t.traceroute_id = 7 ORDER BY hop_number ASC;
        +------------+-------------+-----------+------------+-----------------+--------------+------------------+----------------+----------------------------------+
        | reporter   | origin_ip   | dest_ip   |   probe_id |   traceroute_id |   hop_number | hop_kvs          | host           | cdate                            |
        |------------+-------------+-----------+------------+-----------------+--------------+------------------+----------------+----------------------------------|
        | nm         | 10.0.0.43   | 8.8.8.8   |        257 |               7 |            1 | "time"=>"1.439"  | 10.0.0.1       | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        258 |               7 |            1 | "time"=>"1.598"  | 10.0.0.1       | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        259 |               7 |            1 | "time"=>"1.595"  | 10.0.0.1       | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        263 |               7 |            2 | "time"=>"13.187" | 50.131.116.1   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        265 |               7 |            2 | "time"=>"19.425" | 50.131.116.1   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        264 |               7 |            2 | "time"=>"15.993" | 50.131.116.1   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        260 |               7 |            3 | "time"=>"16.958" | 162.151.31.41  | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        261 |               7 |            3 | "time"=>"17.373" | 162.151.31.41  | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        262 |               7 |            3 | "time"=>"17.713" | 162.151.31.41  | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        271 |               7 |            4 | "time"=>"18.931" | 68.85.57.122   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        270 |               7 |            4 | "time"=>"18.621" | 68.85.154.34   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        269 |               7 |            4 | "time"=>"18.24"  | 68.85.57.122   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        268 |               7 |            5 |                  | 68.86.143.26   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        266 |               7 |            5 | "time"=>"20.194" | 68.86.143.26   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        267 |               7 |            5 |                  | 68.86.143.26   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        272 |               7 |            7 | "time"=>"20.726" | 4.69.152.208   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        276 |               7 |            8 | "time"=>"23.985" | 72.14.223.91   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        277 |               7 |            8 | "time"=>"24.02"  | 72.14.223.91   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        278 |               7 |            8 | "time"=>"24.007" | 72.14.223.91   | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        274 |               7 |            9 | "time"=>"24.001" | 64.233.175.237 | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        273 |               7 |            9 | "time"=>"23.992" | 64.233.175.239 | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        275 |               7 |            9 | "time"=>"23.996" | 72.14.237.189  | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        256 |               7 |           10 | "time"=>"15.905" | 8.8.8.8        | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        254 |               7 |           10 | "time"=>"22.721" | 8.8.8.8        | 2015-02-02 22:52:46.240210-08:00 |
        | nm         | 10.0.0.43   | 8.8.8.8   |        255 |               7 |           10 | "time"=>"23.983" | 8.8.8.8        | 2015-02-02 22:52:46.240210-08:00 |
        +------------+-------------+-----------+------------+-----------------+--------------+------------------+----------------+----------------------------------+

        dev_fzt> SELECT * FROM trv_trace WHERE traceroute_id in (1728) ORDER BY traceroute_id,hop_number ASC;
        | reporter   |   traceroute_id | origin_ip    | dest_ip        |   probe_id |   hop_number | host            | hop_kvs           |
        |:-----------|----------------:|:-------------|:---------------|-----------:|-------------:|:----------------|:------------------|
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38025 |            1 | 192.168.2.1     | "time"=>"77.669"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38023 |            1 | 192.168.2.1     | "time"=>"77.327"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38024 |            1 | 192.168.2.1     | "time"=>"77.357"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38028 |            3 | 129.250.207.57  | "time"=>"121.016" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38026 |            3 | 129.250.207.57  | "time"=>"107.901" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38027 |            3 | 129.250.207.57  | "time"=>"111.664" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38034 |            4 | 129.250.5.238   | "time"=>"121.005" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38033 |            4 | 129.250.5.238   | "time"=>"121.01"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38032 |            4 | 129.250.5.238   | "time"=>"107.885" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38031 |            5 | 129.250.4.119   | "time"=>"120.994" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38030 |            5 | 129.250.4.119   | "time"=>"121.0"   |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38029 |            5 | 129.250.4.119   | "time"=>"121.002" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38040 |            6 | 129.250.193.242 | "time"=>"48.426"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38038 |            6 | 129.250.193.242 | "time"=>"120.983" |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38039 |            6 | 129.250.193.242 | "time"=>"48.277"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38035 |            7 | 208.67.222.222  | "time"=>"54.002"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38036 |            7 | 208.67.222.222  | "time"=>"56.042"  |
        | nm         |            1728 | 192.168.3.61 | 208.67.222.222 |      38037 |            7 | 208.67.222.222  | "time"=>"59.933"  |
        SELECT 18

size of db with 730 traces
    .. code-block:: sql

        dev_fzt> SELECT nspname || '.' || relname AS "relation",
            pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
          FROM pg_class C
          LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
          WHERE nspname NOT IN ('pg_catalog', 'information_schema')
            AND C.relkind <> 'i'
            AND nspname !~ '^pg_toast'
          ORDER BY pg_total_relation_size(C.oid) DESC
          LIMIT 20;
        +--------------------------+--------------+
        | relation                 | total_size   |
        |--------------------------+--------------|
        | public.hop               | 2320 kB      |
        | public.traceroute        | 160 kB       |
        | public.probe_id_seq      | 8192 bytes   |
        | public.traceroute_id_seq | 8192 bytes   |
        | public.annotation        | 8192 bytes   |
        +--------------------------+--------------+
        SELECT 5

Annotations are usually bad, lets find them
    .. code-block:: sql

        traceroutedb> SELECT DISTINCT traceroute_id from hop where (hop_kvs->'anno') IS NOT NULL;
        +-----------------+
        |   traceroute_id |
        |-----------------|
        |              25 |
        +-----------------+
        SELECT 1

Find missing hops
    .. code-block:: sql

        traceroutedb> SELECT previd + 1 as missing FROM ( SELECT DISTINCT hop_number, LAG(hop_number) OVER (ORDER BY hop_number) previd FROM (SELECT DISTINCT hop_number FROM trv_trace WHERE traceroute_id = 1900 ORDER BY hop_number) r ) q WHERE previd <> hop_number - 1 ORDER BY hop_number;
        |   missing |
        |-----------|
        |         7 |
        SELECT 1


Find same routers at same distance between N traces
    .. code-block:: sql

        traceroutedb> SELECT hop_number, ARRAY(SELECT DISTINCT UNNEST(array_agg(host))) FROM trv_trace WHERE traceroute_id IN (1904, 1903) GROUP BY hop_number ORDER BY hop_number;
        |   hop_number | array                                                                       |
        |--------------+-----------------------------------------------------------------------------|
        |            1 | {192.168.43.1}                                                              |
        |            2 | {172.26.96.169}                                                             |
        |            3 | {172.16.157.164}                                                            |
        |            4 | {12.249.2.49}                                                               |
        |            5 | {12.83.180.82}                                                              |
        |            6 | {12.122.137.181}                                                            |
        |            7 | {12.250.31.10}                                                              |
        |            8 | {209.85.244.23,209.85.241.171}                                              |
        |            9 | {64.233.174.43,216.239.49.123,216.239.56.127,216.239.56.123,209.85.255.255} |
        |           10 | {8.8.8.8}                                                                   |
        SELECT 10


Aggregate times from hops
    .. code-block:: sql

        traceroutedb> SELECT hop_number,host,array_agg(cast(hop_kvs->'time' as double precision)) as time FROM trv_trace WHERE traceroute_id IN (634) GROUP BY host,traceroute_id,hop_number ORDER BY traceroute_id,hop_number;
        |   hop_number | host          | time                        |
        |-------------:|:--------------|:----------------------------|
        |            1 | 192.168.88.1  | [1.936, 1.942, 1.951]       |
        |            2 | 10.0.0.1      | [1.921, 1.927, 1.933]       |
        |            3 | 96.120.89.253 | [14.356, 40.597, 9.585]     |
        |            4 | 162.151.31.33 | [40.776, 40.778, 40.707]    |
        |            5 | 68.87.193.129 | [42.149, 41.617, 42.142]    |
        |            6 | 68.86.90.93   | [10.756, 37.888, 41.095]    |
        |            7 | 68.86.87.158  | [17.67, 17.664, 17.689]     |
        |            8 | 68.86.86.222  | [17.318, 15.512, 17.035]    |
        |            9 | 66.208.216.42 | [19.326]                    |
        |            9 | 66.208.216.38 | [21.398]                    |
        |            9 | 66.208.216.34 | [21.353]                    |
        SELECT 11
