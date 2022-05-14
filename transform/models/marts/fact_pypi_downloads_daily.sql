SELECT
      DATE(raw.timestamp)           AS download_date,
      DATE(DATE_ADD(raw.timestamp, INTERVAL ((-1 * EXTRACT(DAYOFWEEK FROM timestamp)) + 1) DAY))
                                    AS week_end_date,
      project,
      count(*)                      AS num_downloads
FROM `bigquery-public-data.pypi.file_downloads` raw
WHERE project IN ('meltano', 'singer-sdk')
  AND DATE(timestamp) > "2020-06-01"
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 3
