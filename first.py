import xmlrpc.client
import ssl
import time
import configparser
import os
import re
from datetime import datetime

# Read configuration from config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

WIKI_URL = config.get('dokuwiki', 'url')
USERNAME = config.get('dokuwiki', 'username')
PASSWORD = config.get('dokuwiki', 'password')

# Create URL with basic auth
WIKI_URL_WITH_AUTH = f"https://{USERNAME}:{PASSWORD}@{WIKI_URL.split('://')[-1]}"

# Create an SSL context that doesn't verify certificates
context = ssl._create_unverified_context()
server = xmlrpc.client.ServerProxy(WIKI_URL_WITH_AUTH, context=context)

def fix_page_content(content):
    """
    Apply fixes to page content.
    Look for "Updated: DATE" at the bottom and replace with current date.
    If not found, add it.
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    update_line = f"//Updated: {current_date}//"
    
    # Split content into lines
    lines = content.split('\n')
    
    # Search for "Updated:" pattern in the last 10 lines (bottom of page)
    updated_found = False
    for i in range(max(0, len(lines) - 10), len(lines)):
        # Match patterns like "//Updated: February 20, 2026//" or "Updated: February 20, 2026"
        if re.search(r'(?://)?Updated:\s*[A-Za-z]+\s+\d{1,2},\s+\d{4}(?://)?', lines[i], re.IGNORECASE):
            lines[i] = update_line
            updated_found = True
            break
    
    # If no "Updated:" line found at the bottom, add it
    if not updated_found:
        # Remove trailing empty lines first
        while lines and lines[-1].strip() == '':
            lines.pop()
        lines.append('')
        lines.append(update_line)
    
    return '\n'.join(lines)

try:
    # Test connection with getVersion
    version = server.dokuwiki.getVersion()
    print(f"Connected to DokuWiki version: {version}\n")
    
    # Get all pages (using the correct method)
    print("Fetching all pages...")
    all_pages = server.dokuwiki.getPagelist('', {})  # Empty string gets all namespaces
    print(f"Found {len(all_pages)} pages\n")
    
    # Process each page
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for page_info in all_pages:
        page_id = page_info['id']
        print(f"Processing: {page_id}")
        
        try:
            # Download page content
            original_content = server.wiki.getPage(page_id)
            
            # Fix the content
            fixed_content = fix_page_content(original_content)
            
            # Only update if content changed
            if fixed_content != original_content:
                server.wiki.putPage(
                    page_id,
                    fixed_content,
                    {"sum": "Automated fixes via Python", "minor": True}
                )
                print(f"  ✓ Updated: {page_id}")
                updated_count += 1
            else:
                print(f"  - No changes needed: {page_id}")
                skipped_count += 1
            
            # Add small delay to avoid overwhelming the server
            time.sleep(0.1)
            
        except Exception as e:
            print(f"  ✗ Error processing {page_id}: {e}")
            error_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Total pages: {len(all_pages)}")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped (no changes): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"{'='*50}")
    
except xmlrpc.client.ProtocolError as err:
    print(f"Protocol Error {err.errcode}: {err.errmsg}")
    print("Check: 1) XML-RPC enabled ($conf['xmlrpc']=1)")
    print("       2) Remote API enabled ($conf['remoteuser']='@ALL')")
    print("       3) User has write permissions for the namespace")
except Exception as e:
    print(f"Error: {e}")