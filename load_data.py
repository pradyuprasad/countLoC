import json

def sum_contributions_by_filetype():
   # Load the JSON data
   with open('contribution_stats.json', 'r') as f:
       data = json.load(f)

   # Dictionary to store total contributions by file type
   filetype_stats = {}

   # Set of code file extensions to track
   code_extensions = {
       '.py',    # Python
       '.java',  # Java
       '.go',    # Go
       '.tsx',   # TypeScript React
       '.js',    # JavaScript
       '.css',   # CSS
       '.html',  # HTML
   }

   # Iterate through all repositories and users
   for repo in data.values():
       if isinstance(repo, dict):  # Skip empty repositories
           for user_stats in repo.values():
               if isinstance(user_stats, dict):
                   for filetype, changes in user_stats.items():
                       if isinstance(changes, dict):
                           # Initialize filetype in dictionary if not exists
                           if filetype not in filetype_stats:
                               filetype_stats[filetype] = {
                                   'additions': 0,
                                   'deletions': 0,
                                   'net_changes': 0
                               }

                           # Add up the contributions
                           filetype_stats[filetype]['additions'] += changes.get('additions', 0)
                           filetype_stats[filetype]['deletions'] += changes.get('deletions', 0)
                           filetype_stats[filetype]['net_changes'] += changes.get('additions', 0) - changes.get('deletions', 0)

   # Sort by net changes
   sorted_stats = sorted(filetype_stats.items(), key=lambda x: abs(x[1]['net_changes']), reverse=True)

   # Print all file types first
   print("All File Type Statistics (sorted by absolute net changes):")
   print("-" * 65)
   print(f"{'File Type':<15} {'Additions':>12} {'Deletions':>12} {'Net Changes':>12}")
   print("-" * 65)

   for filetype, stats in sorted_stats:
       print(f"{filetype:<15} {stats['additions']:>12,d} {stats['deletions']:>12,d} {stats['net_changes']:>12,d}")

   # Print code files only
   print("\nCode File Statistics Only:")
   print("-" * 65)
   print(f"{'File Type':<15} {'Additions':>12} {'Deletions':>12} {'Net Changes':>12}")
   print("-" * 65)

   total_net_changes = 0
   for filetype, stats in sorted_stats:
       if filetype in code_extensions:
           print(f"{filetype:<15} {stats['additions']:>12,d} {stats['deletions']:>12,d} {stats['net_changes']:>12,d}")
           total_net_changes += stats['net_changes']

   print("-" * 65)
   print(f"{'Total':<15} {' ':>12} {' ':>12} {total_net_changes:>12,d}")

if __name__ == "__main__":
   sum_contributions_by_filetype()
