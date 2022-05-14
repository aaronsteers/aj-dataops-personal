SELECT
      week_end_date,
      project,
      sum(num_downloads) AS num_downloads
FROM {{ ref('fact_pypi_downloads_daily') }}
GROUP BY 1, 2
HAVING COUNT(DISTINCT download_date) = 7 # Only show full weeks
ORDER BY 1 DESC, 2
