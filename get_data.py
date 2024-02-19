"""Use PyAirbyte to source data from GitHub."""

import airbyte as ab


REPOS = [
    "airbytehq/quickstarts",
]
ENV_GITHUB_PERSONAL_ACCESS_TOKEN = "GITHUB_PERSONAL_ACCESS_TOKEN"
CACHE_NAME = "my_data"


def get_github_data(cache) -> ab.ReadResult:
    """Get data from GitHub."""
    print("Getting data from GitHub...")
    source_github = ab.get_source("source-github")
    source_github.set_config(
        {
            "owner": "airbytehq",
            "repositories": REPOS,
            "start_date": "2024-01-01T00:00:00Z",
            "credentials": {
                "personal_access_token": str(
                    ab.get_secret(ENV_GITHUB_PERSONAL_ACCESS_TOKEN)
                )
            },
        }
    )
    source_github.select_streams(["pull_requests", "issues"])
    return source_github.read(cache=cache)


def main():
    """Main function."""
    cache = ab.new_local_cache(CACHE_NAME)
    read_result = get_github_data(cache=cache)


if __name__ == "__main__":
    main()
