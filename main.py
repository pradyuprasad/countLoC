import os
import git
import shutil
from datetime import datetime
import subprocess
from collections import defaultdict
import time
import json

from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_PAT")
username = 'pradyu'

# Keep track of skipped usernames
skipped_users = set()

def list_repositories():
   """
   Fetch list of repositories using GitHub API
   """
   import requests
   headers = {
       "Authorization": f"Bearer {GITHUB_TOKEN}",
       "Accept": "application/vnd.github+json"
   }

   print("\n🔍 Scanning GitHub account for repositories...")
   url = "https://api.github.com/user/repos"
   repos = []
   page = 1
   while url:
       print(f"📚 Fetching page {page}...")
       response = requests.get(url, headers=headers)
       response.raise_for_status()
       current_repos = response.json()
       print(f"✨ Found {len(current_repos)} repositories")
       repos.extend(current_repos)
       url = response.links.get('next', {}).get('url')
       page += 1

   print(f"📊 Total repositories found: {len(repos)}")
   return repos

def clone_repository(clone_url, repo_name):
   """
   Clone repository to a subdirectory
   """
   target_dir = os.path.join('repos', repo_name)
   if os.path.exists(target_dir):
       print(f"🗑️  Cleaning up existing directory for {repo_name}")
       shutil.rmtree(target_dir)

   print(f"📂 Creating directory for {repo_name}")
   os.makedirs(target_dir, exist_ok=True)

   print(f"⬇️  Cloning {repo_name}...")
   if GITHUB_TOKEN:
       clone_url = clone_url.replace('https://', f'https://{GITHUB_TOKEN}@')

   git.Repo.clone_from(clone_url, target_dir)
   print(f"✅ Clone complete for {repo_name}")
   return target_dir

def get_file_changes_by_extension(repo_path):
   """
   Get number of lines changed by file extension for each user
   """
   changes_by_user = defaultdict(lambda: defaultdict(lambda: {'additions': 0, 'deletions': 0}))
   repo = git.Repo(repo_path)

   print("\n🕒 Analyzing commits from 2024...")
   commits = list(repo.iter_commits(since="2024-01-01"))
   print(f"📝 Found {len(commits)} commits in 2024")

   for commit in commits:
       commit_date = datetime.fromtimestamp(commit.committed_date)
       if commit_date.year != 2024:
           continue

       author_id = f"{commit.author.name} <{commit.author.email}>"

       # Check if commit is by username
       if username not in author_id.lower():
           skipped_users.add(author_id)
           continue

       print(f"\n📌 Processing commit by {author_id}")
       print(f"🗓️  Date: {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
       print(f"💬 Message: {commit.message.split()[0]}...")

       try:
           for file in commit.stats.files:
               ext = os.path.splitext(file)[1]
               if not ext:
                   ext = 'no_extension'
               else:
                   ext = ext.lower()

               adds = commit.stats.files[file]['insertions']
               dels = commit.stats.files[file]['deletions']

               if adds > 0 or dels > 0:
                   print(f"   📊 {file}: +{adds} -{dels}")

               changes_by_user[author_id][ext]['additions'] += adds
               changes_by_user[author_id][ext]['deletions'] += dels
       except Exception as e:
           print(f"⚠️  Error processing commit {commit.hexsha[:8]}: {e}")
           continue

   return dict(changes_by_user)

def main():
   print("\n🚀 Starting code analysis...")
   os.makedirs('repos', exist_ok=True)

   global_stats = {}
   repositories = list_repositories()

   for i, repo in enumerate(repositories, 1):
       print(f"\n{'='*50}")
       print(f"📦 Repository {i}/{len(repositories)}: {repo['name']}")
       print(f"{'='*50}")

       try:
           repo_path = clone_repository(repo['clone_url'], repo['name'])
           repo_stats = get_file_changes_by_extension(repo_path)

           print("\n📊 Repository Statistics:")
           for user, extensions in repo_stats.items():
               print(f"\n👤 {user}:")
               for ext, stats in extensions.items():
                   print(f"   {ext}: +{stats['additions']} -{stats['deletions']}")

           global_stats[repo['name']] = repo_stats

           print(f"\n🧹 Cleaning up {repo['name']}")
           shutil.rmtree(repo_path)

           # Save progress after each repo
           with open('contribution_stats.json', 'w') as f:
               json.dump(global_stats, f, indent=2)
           print("💾 Progress saved to contribution_stats.json")

           # Save skipped users after each repo
           with open('skipped_users.json', 'w') as f:
               json.dump(list(skipped_users), f, indent=2)
           print("📝 Skipped users saved to skipped_users.json")

       except Exception as e:
           print(f"❌ Error processing {repo['name']}: {e}")
           if os.path.exists(os.path.join('repos', repo['name'])):
               shutil.rmtree(os.path.join('repos', repo['name']))

   print("\n🎉 Analysis complete!")
   print("\n💾 Final statistics saved to contribution_stats.json")
   print(f"\n👥 Found {len(skipped_users)} unique non-pradyu contributors (saved to skipped_users.json)")

   if os.path.exists('repos'):
       print("\n🧹 Final cleanup...")
       shutil.rmtree('repos')

if __name__ == "__main__":
   main()
