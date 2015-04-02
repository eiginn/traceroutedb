# Traceroute DB

[![Code Health](https://landscape.io/github/eiginn/traceroutedb/master/landscape.svg?style=flat)](https://landscape.io/github/eiginn/traceroutedb/master)
## Some examples
find traceroutes where any hop is over a time
```
dev_fzt> SELECT * FROM traceroute WHERE traceroute_id in (SELECT DISTINCT traceroute_id FROM hop where (hop_kvs->'time')::float > 10);
+-----------------+-------------+---------------+----------------------------------+------------+
|   traceroute_id | origin_ip   | dest_ip       | cdate                            | reporter   |
|-----------------+-------------+---------------+----------------------------------+------------|
|               6 | 10.0.0.43   | 173.245.48.10 | 2015-02-02 22:15:17.632821-08:00 | nm         |
|               7 | 10.0.0.43   | 8.8.8.8       | 2015-02-02 22:52:46.240210-08:00 | nm         |
+-----------------+-------------+---------------+----------------------------------+------------+
```

find full traceroute like output
```
dev_fzt> SELECT t.reporter, t.origin_ip, t.dest_ip, hop.* from traceroute as t INNER JOIN hop on t.traceroute_id = hop.traceroute_id WHERE t.traceroute_id = 7 ORDER BY hop_number ASC;
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
```
