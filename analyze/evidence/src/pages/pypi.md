# Interesting PyPi Stats

```pypi_downloads_query
SELECT
      #  -  + 1 as download_date,
      DATE(DATE_ADD(timestamp, INTERVAL ((-1 * EXTRACT(DAYOFWEEK FROM timestamp)) + 1) DAY)) as download_date,
      project,
      count(*) downloads
FROM `bigquery-public-data.pypi.file_downloads` 
WHERE project IN ('meltano', 'singer-sdk')
  AND DATE(timestamp) BETWEEN "2022-01-02" AND "2022-04-23"
GROUP BY 1, 2
ORDER BY 1 DESC, 2
## LIMIT 1000
```

## Meltano Stats

<LineChart 
    data={data.pypi_downloads_query.filter(p => p.project === 'meltano')}  
    x=download_date 
    y=downloads
/>

## SDK Stats

<LineChart 
    data={data.pypi_downloads_query.filter(p => p.project === 'singer-sdk')}  
    x=download_date 
    y=downloads
/>
