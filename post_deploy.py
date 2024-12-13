# post_deploy.py
import os
import subprocess
from datetime import datetime, timedelta, timezone

def get_recent_posts(posts_directory, days=5):
    # Calculate the cutoff date and make it timezone-aware
    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days))

    # List to store the formatted paths
    formatted_paths = []

    # Iterate over all files in the posts directory
    for filename in os.listdir(posts_directory):
        file_path = os.path.join(posts_directory, filename)

        # Check if it's a file
        if os.path.isfile(file_path):
            # Get the git creation date of the file
            try:
                # Get the creation date for the file (first commit that added the file)
                commit_date_str = subprocess.check_output(
                    ['git', 'log', '--format=%cd', '--date=iso', '--diff-filter=A', '-n', '1', filename],
                    cwd=posts_directory
                ).decode('utf-8').strip()
                
                # Parse the commit date and make it timezone-aware
                commit_date = datetime.fromisoformat(commit_date_str).replace(tzinfo=timezone.utc)

                # Check if the commit date is within the cutoff date
                if commit_date >= cutoff_date:
                    # Extract metadata from the file (assuming it's in YAML front matter)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        # Extract slug and created date from the metadata
                        slug = extract_metadata(content, 'slug')
                        created_date = extract_metadata(content, 'date', 'created')

                        if slug and created_date:
                            # Format the date and create the path
                            created_date_obj = datetime.fromisoformat(created_date).replace(tzinfo=timezone.utc)
                            formatted_path = f"{created_date_obj.year}/{created_date_obj.month:02}/{created_date_obj.day:02}/{slug}.html"
                            formatted_paths.append(formatted_path)

            except subprocess.CalledProcessError:
                print(f"Error retrieving git info for {filename}")

    return formatted_paths

def extract_metadata(content, key, subkey=None):
    """Extract metadata from the content."""
    lines = content.splitlines()
    metadata = {}
    in_metadata = False

    for line in lines:
        if line.strip() == '---':
            in_metadata = not in_metadata
            continue
        if in_metadata:
            if ':' in line:
                k, v = line.split(':', 1)
                metadata[k.strip()] = v.strip()

    if subkey:
        return metadata.get(key, {}).get(subkey)
    return metadata.get(key)

def main():
    posts_directory = 'docs/posts'  # Update this path
    recent_posts = get_recent_posts(posts_directory)

    # Print all entries in the list
    for entry in recent_posts:
        print(entry)

if __name__ == "__main__":
    main()
