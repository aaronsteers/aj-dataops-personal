"""Use PyAirbyte to source data from GitHub.

Usage:
  poetry run python get_data.py
"""

import airbyte as ab


ENV_GITHUB_PERSONAL_ACCESS_TOKEN = "GITHUB_PERSONAL_ACCESS_TOKEN"
GITHUB_CONFIG = {
    # https://docs.airbyte.com/integrations/sources/github#reference
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
    read_result = ab.get_source(
        "source-github",
        config=GITHUB_CONFIG,
        streams=["pull_requests", "issues"],
    ).read()
    print(f"Finished reading GitHub data into '{read_result.cache.config.db_path}'.")
    for stream in read_result.streams.values():
        tbl = stream.to_sql_table()
        print(
            f"{(stream.stream_name + ':'):15}{len(stream):7,} records ({tbl.fullname})"
        )


if __name__ == "__main__":
    main()
