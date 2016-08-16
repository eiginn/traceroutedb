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

        traceroutedb> SELECT * FROM traceroute WHERE traceroute_id in (SELECT DISTINCT traceroute_id FROM hop where (hop_kvs->'time')::float > 10);
        +-----------------+-------------+---------------+----------------------------------+------------+
        |   traceroute_id | origin_ip   | dest_ip       | cdate                            | reporter   |
        |-----------------+-------------+---------------+----------------------------------+------------|
        |               6 | 10.0.0.43   | 173.245.48.10 | 2015-02-02 22:15:17.632821-08:00 | nm         |
        |               7 | 10.0.0.43   | 8.8.8.8       | 2015-02-02 22:52:46.240210-08:00 | nm         |
        +-----------------+-------------+---------------+----------------------------------+------------+

find full traceroute like output
    .. code-block:: sql

        traceroutedb> SELECT * FROM trv_trace WHERE traceroute_id = 186 ORDER BY hop_number,probe_id;
        | reporter   |   traceroute_id | origin_ip   | dest_ip   |   probe_id |   hop_number | host           | hop_kvs                          |
        |:-----------|----------------:|:------------|:----------|-----------:|-------------:|:---------------|:---------------------------------|
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4924 |            1 | 10.0.0.1       | "time"=>"1.166"                  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4925 |            1 | 10.0.0.1       | "time"=>"1.185"                  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4926 |            1 | 10.0.0.1       | "time"=>"1.165"                  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4930 |            2 | 96.120.89.253  | "asn"=>"7922", "time"=>"9.867"   |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4931 |            2 | 96.120.89.253  | "asn"=>"7922", "time"=>"14.331"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4932 |            2 | 96.120.89.253  | "asn"=>"7922", "time"=>"15.23"   |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4927 |            3 | 162.151.31.33  | "asn"=>"7922", "time"=>"15.43"   |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4928 |            3 | 162.151.31.33  | "asn"=>"7922", "time"=>"15.591"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4929 |            3 | 162.151.31.33  | "asn"=>"7922", "time"=>"15.589"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4933 |            4 | 68.87.193.129  | "asn"=>"7922", "time"=>"16.151"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4934 |            4 | 68.87.193.129  | "asn"=>"7922", "time"=>"16.333"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4935 |            4 | 68.87.193.129  | "asn"=>"7922", "time"=>"16.447"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4939 |            6 | 68.86.86.166   | "asn"=>"7922", "time"=>"18.941"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4940 |            6 | 68.86.84.14    | "asn"=>"7922", "time"=>"11.172"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4941 |            6 | 68.86.86.30    | "asn"=>"7922", "time"=>"11.204"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4936 |            7 | 66.208.228.70  | "asn"=>"7922", "time"=>"17.687"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4937 |            7 | 66.208.228.70  | "asn"=>"7922", "time"=>"18.828"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4938 |            7 | 66.208.228.70  | "asn"=>"7922", "time"=>"18.6"    |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4945 |            8 | 216.239.49.11  | "asn"=>"15169", "time"=>"19.17"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4946 |            8 | 216.239.49.11  | "asn"=>"15169", "time"=>"19.479" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4947 |            8 | 216.239.49.11  | "asn"=>"15169", "time"=>"19.03"  |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4942 |            9 | 216.239.49.83  | "asn"=>"15169", "time"=>"20.089" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4943 |            9 | 216.239.58.195 | "asn"=>"15169", "time"=>"20.409" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4944 |            9 | 216.239.58.213 | "asn"=>"15169", "time"=>"19.804" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4921 |           10 | 8.8.8.8        | "asn"=>"15169", "time"=>"19.349" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4922 |           10 | 8.8.8.8        | "asn"=>"15169", "time"=>"19.298" |
        | wintermute |             186 | 10.0.0.90   | 8.8.8.8   |       4923 |           10 | 8.8.8.8        | "asn"=>"15169", "time"=>"19.597" |
        SELECT 27

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

Find missing hops (though this has questionable utility)
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

        traceroutedb> SELECT hop_number,json_build_object(host,json_agg(cast(hop_kvs->'time' as double precision))) as time FROM trv_trace WHERE traceroute_id IN (100) GROUP BY host,traceroute_id,hop_number ORDER BY traceroute_id,hop_number;
        |   hop_number | time                                            |
        |-------------:|:------------------------------------------------|
        |            1 | {"10.0.0.1" : [3.568, 3.189, 3.053]}            |
        |            2 | {"96.120.89.253" : [18.729, 18.064, 11.431]}    |
        |            3 | {"162.151.31.33" : [19.332, 19.331, 18.952]}    |
        |            4 | {"68.87.193.129" : [20.54, 21.1, 19.922]}       |
        |            5 | {"68.86.90.93" : [19.491]}                      |
        |            6 | {"68.86.87.158" : [14.088, 20.12, 29.474]}      |
        |            7 | {"68.86.88.190" : [18.398, 18.772, 18.01]}      |
        |            8 | {"66.208.216.38" : [20.68]}                     |
        |            8 | {"66.208.216.42" : [20.624]}                    |
        |            8 | {"66.208.216.34" : [20.613]}                    |
        |            9 | {"202.97.50.73" : [19.168, 20.45, 19.843]}      |
        |           10 | {"202.97.51.229" : [165.616]}                   |
        |           12 | {"202.97.33.17" : [178.856, 178.248, 179.682]}  |
        |           13 | {"61.152.86.193" : [172.432, 170.878, 173.214]} |
        SELECT 14
