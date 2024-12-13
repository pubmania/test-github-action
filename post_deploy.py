# post_deploy.py
import re
import os
import yaml
import datetime

def get_yaml_frontmatter(path):
    # Regex to match YAML front matter
    yaml_regex = re.compile(r'^(---\n.*?\n---\n)', re.DOTALL)

    # Check if the path is a directory or a file
    if os.path.isdir(path):
        # If it's a directory, process all .md files
        for filename in os.listdir(path):
            if filename.endswith('.md'):
                file_path = os.path.join(path, filename)
                process_file_yaml(file_path, yaml_regex)
    elif os.path.isfile(path) and path.endswith('.md'):
        # If it's a single .md file, process it
        process_file_yaml(path, yaml_regex)
    else:
        print("Provided path is neither a valid directory nor a .md file.")

def process_file_yaml(file_path, yaml_regex):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find YAML front matter
    match = yaml_regex.search(content)
    if match:
        frontmatter = match.group(1)
        # Parse the existing YAML front matter
        frontmatter_content = frontmatter.split('---')[1].strip()
        frontmatter_dict = yaml.safe_load(frontmatter_content)
        for key, value in frontmatter_dict.items():
            if key == 'date':
                created_date = value['created']
            if key == 'slug':
                slug_value = value
        print(f"created_date: {created_date} and slug_value: {slug_value}")
        yyyy = created_date.year
        mm = f"{created_date.month:02}"
        dd = f"{created_date.day:02}"
        print(f"{yyyy}/{mm}/{dd}/{slug_value}.html")
        print(f"assets/images/social/posts/{file_path.split('.')[0]}.png")
    else:
        print(f"No YAML front matter found in: {file_path}")

def main():
    posts_directory = 'docs/posts'  # Update this path
    path = 'docs/posts'
    get_yaml_frontmatter(path)

if __name__ == "__main__":
    main()
