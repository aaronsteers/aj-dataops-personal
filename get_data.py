"""Use PyAirbyte to source data from GitHub.

Usage:
  poetry run python get_data.py
"""

import airbyte as ab


ENV_GITHUB_PERSONAL_ACCESS_TOKEN = "GITHUB_PERSONAL_ACCESS_TOKEN"
CACHE_NAME = "my_data"
GITHUB_CONFIG = {
    "start_date": "2024-01-01T00:00:00Z",
    "repositories": [
        "airbytehq/quickstarts",
    ],
    "credentials": {
        "personal_access_token": ab.get_secret(ENV_GITHUB_PERSONAL_ACCESS_TOKEN)
    },
}



def main():
    """Main function."""
    print("Getting data from GitHub...")
    source_github = ab.get_source("source-github")
    source_github.set_config(GITHUB_CONFIG)
    source_github.select_streams(["pull_requests", "issues"])
    cache = ab.new_local_cache(CACHE_NAME)
    read_result = source_github.read(cache=cache)
    print("Finished getting data from GitHub.")
    for stream in read_result.streams.values():
        tbl = stream.to_sql_table()
        print(
            f"{(stream.stream_name + ':'):15}{len(stream):7,} records ({tbl.fullname})"
        )


if __name__ == "__main__":
    main()
