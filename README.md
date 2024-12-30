# GitHub Contribution Analyzer

A Python-based CLI tool that analyzes GitHub repositories to track code contributions by file type, filtering for a specific username.

## Features

- Automatically scans all repositories in your GitHub account
- Tracks line changes (additions/deletions) by file extension
- Filters contributions by specified username
- Generates detailed statistics for both code and non-code files
- Saves progress incrementally to prevent data loss
- Provides clean, formatted output of contribution statistics

## Prerequisites

- Python 3.x
- GitHub Personal Access Token (PAT)

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd github-contribution-analyzer
```

2. Install required dependencies:

```
pip install gitpython python-dotenv requests
```

3. Create a .env file in the project root and add your GitHub PAT:

```
GITHUB_PAT=your_github_personal_access_token
```


# Usage
1. Run the main analysis script:
```
python main.py
```

2. View the statistics:

```
python load_data.py
```

The tool will:
* Scan through all your GitHub repositories
* Clone each repository temporarily
* Analyze commits from 2024
* Generate statistics for file changes
* Save results to `contribution_stats.json`
* Track non-matching users in `skipped_users.json`

## Output Files

* `contribution_stats.json`: Contains detailed statistics about contributions by file type
* `skipped_users.json`: Lists contributors who don't match the specified username

## Limitations

* Only analyzes commits from 2024 onwards
* Filters for a specific username
* Requires repository access through GitHub PAT

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
