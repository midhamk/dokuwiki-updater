# DokuWiki Updater

A Python script to automatically update all pages in a DokuWiki instance via XML-RPC API.

## Features
- Downloads all pages from DokuWiki
- Updates "Updated: DATE" line at the bottom of each page
- Reads credentials from config file
- Shows summary of updated/skipped/error pages

## Setup

1. Create a `config.ini` file with your DokuWiki credentials:
```ini
[dokuwiki]
url = https://your-server/dokuwiki/lib/exe/xmlrpc.php
username = your_username
password = your_password
```

2. Install Python 3 (if not already installed)

3. Run the script:
```bash
python first.py
```

## Requirements
- Python 3.6+
- DokuWiki with XML-RPC enabled

## Configuration
Edit your DokuWiki's `conf/local.php` and add:
```php
$conf['xmlrpc'] = 1;
$conf['remoteuser'] = '@ALL';
```

## Security
⚠️ Never commit `config.ini` to version control as it contains credentials.
