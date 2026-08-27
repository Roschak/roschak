import os
import re

cert_dir = 'certificates'
readme_path = 'README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    readme_content = f.read()

for filename in os.listdir(cert_dir):
    if not filename.endswith('.jpg'):
        continue
    
    # Generate clean name
    name, ext = os.path.splitext(filename)
    # Replace any non-alphanumeric character with underscore
    clean_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    # Remove multiple underscores
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    clean_filename = clean_name + ext
    
    if clean_filename == filename:
        continue
        
    old_path = os.path.join(cert_dir, filename)
    new_path = os.path.join(cert_dir, clean_filename)
    
    # Rename file
    try:
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {clean_filename}")
    except Exception as e:
        print(f"Failed to rename {filename}: {e}")
        continue
        
    # Replace in README.md
    # Need to handle URL encoded version in README
    # Just to be safe, find the <img> tag that contains this filename or something similar.
    # Actually, the python script earlier used urllib.parse.quote. Let's just find the exact string that was in README.
    
    # Let's do a regex search for the old filename in the README, considering URL encoding.
    import urllib.parse
    encoded_filename = urllib.parse.quote(filename)
    
    # Some spaces might be %20, some brackets %5B.
    # Replace in readme_content
    if encoded_filename in readme_content:
        readme_content = readme_content.replace(f"./certificates/{encoded_filename}", f"./certificates/{clean_filename}")
        print(f"Updated README for {filename} (URL encoded)")
    elif filename in readme_content:
        readme_content = readme_content.replace(f"./certificates/{filename}", f"./certificates/{clean_filename}")
        print(f"Updated README for {filename} (Raw)")
    else:
        # Fallback: maybe spaces are %20 but some chars are not encoded.
        # Just replace the specific img src if it ends with the name (ignoring URL encoding differences)
        # This is harder. Let's manually replace the known ones if they fail.
        pass

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("Done sanitizing.")
