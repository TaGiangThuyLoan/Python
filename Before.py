from github import Github
import csv
import time
from datetime import datetime

# Replace with your GitHub access token
access_token = "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"

# Create a GitHub instance using the access token
g = Github(access_token)

# Define repository details
repo_owner = 'jwasham'
repo_name = 'coding-interview-university'

# Get the repository object
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Function to handle rate limit
def handle_rate_limit(g):
    rate_limit = g.get_rate_limit().core
    if rate_limit.remaining == 0:
        sleep_time = (rate_limit.reset - datetime.utcnow()).total_seconds() + 10
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

# Create CSV file and write the header
with open('Before.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["sha", "author", "author_email", "author_date", "commit_message", "committer", "committer_date", "files_changed"])

    # Use pagination to fetch all commits
    commits = repo.get_commits()
    for commit in commits:
        try:
            handle_rate_limit(g)

            files_changed = [file.filename for file in commit.files]

            commit_info = [
                commit.sha,
                commit.commit.author.name if commit.commit.author else None,
                commit.commit.author.email if commit.commit.author else None,
                commit.commit.author.date,
                commit.commit.message,
                commit.commit.committer.name if commit.commit.committer else None,
                commit.commit.committer.date,
                ', '.join(files_changed)  # Join file names with a comma
            ]

            # Write commit information to CSV file
            writer.writerow([str(item).encode('utf-8').decode('utf-8') for item in commit_info])
            print(commit_info)

        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(5)
            continue

print("Commit information has been saved to Before.csv")
