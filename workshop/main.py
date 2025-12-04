#!/usr/bin/env python3
import sys, re
from datetime import datetime

# Read input from stdin
text = sys.stdin.read()
commits = []
current = []

for line in text.split('\n'):
    # Start new commit when we see "commit" followed by 40 hex chars + optional [source: ...]
    if re.match(r'^commit [0-9a-f]{40}(?: \[source: [^\]]+\])?$', line.strip()):
        if current:
            commits.append('\n'.join(current).rstrip('\n'))
        current = [line]
    elif current:  # Only add lines if we're inside a commit block
        current.append(line)

# Add last commit
if current:
    commits.append('\n'.join(current).rstrip('\n'))

# Sort by date
commits.sort(key=lambda c: (
    datetime.strptime(
        ' '.join(m.groups()),
        "%b %d %H:%M:%S %Y"
    ) if (m := re.search(r'Date:\s+\w{3}\s+(\w{3})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\d{4})', c))
    else datetime.min
))

# Write to output file
output_filename = "sorted_commits.txt"
with open(output_filename, 'w') as f:
    f.write('\n\n'.join(commits))

print(f"Sorted {len(commits)} commits written to {output_filename}", file=sys.stderr)