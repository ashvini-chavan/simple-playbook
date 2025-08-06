import os
from atlassian import Confluence

# Read variables from variables.txt
with open('variables.txt', 'r') as file:
    variables = {}
    for line in file:
        key, value = line.strip().split('=', 1)
        variables[key] = value

username = variables['username']
password = variables['password']
selected_quarter = variables['selected_quarter']
qbr_year = variables['qbr_year']

# Set Confluence URL and space key
confluence_url = 'https://ashviniaws.atlassian.net/wiki'
space_key = 'testspace'

# Fixed parent page ID under which all pages will be created
parent_page_id = '851994'

# Initialize Confluence client
confluence = Confluence(
    url=confluence_url,
    username=username,
    password=password
)

# Find all HTML files in current directory
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# Create or update a page for each HTML file under the fixed parent page
for html_file in html_files:
    page_title = os.path.splitext(html_file)[0]  # Remove .html extension
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Check if child page exists under the space
    existing_page = confluence.get_page_by_title(space=space_key, title=page_title)

    if existing_page:
        # Update existing page
        confluence.update_page(
            page_id=existing_page['id'],
            title=page_title,
            body=html_content,
            parent_id=parent_page_id,
            minor_edit=True
        )
    else:
        # Create new page under the fixed parent page
        confluence.create_page(
            space=space_key,
            title=page_title,
            body=html_content,
            parent_id=parent_page_id
        )
