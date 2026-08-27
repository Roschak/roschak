import re

# Read original README
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the entire block from <style> to </div>
match = re.search(r'<style>.*?</style>\s*<div class="cert-grid">(.*?)</div>', content, re.DOTALL)
if not match:
    print("Could not find the style/grid block")
    exit(1)

full_block = match.group(0)
cards_content = match.group(1)

# Extract each card's details
# <a href="..." ...> <div ...> <img src="..." alt="..." /> </div> <div ...> <div class="cert-title">...</div> <div class="cert-issuer">...</div> </div> </a>
card_pattern = re.compile(
    r'<a href="([^"]+)".*?<img src="([^"]+)" alt="([^"]*)".*?<div class="cert-title">([^<]+)</div>\s*<div class="cert-issuer">([^<]*)</div>',
    re.DOTALL
)

certs = []
for m in card_pattern.finditer(cards_content):
    certs.append({
        'href': m.group(1).strip(),
        'img': m.group(2).strip(),
        'alt': m.group(3).strip(),
        'title': m.group(4).strip(),
        'issuer': m.group(5).strip()
    })

# Build HTML table
html_table = "<table>\n"
for i in range(0, len(certs), 3):
    html_table += "  <tr>\n"
    for j in range(3):
        if i + j < len(certs):
            cert = certs[i + j]
            # using <img> without object-fit since inline style is stripped, but we can set width="100%"
            html_table += f"""    <td align="center" width="33%">
      <a href="{cert['href']}">
        <img src="{cert['img']}" width="100%" alt="{cert['alt']}" />
      </a>
      <br><br>
      <strong>{cert['title']}</strong>
      <br>
      {cert['issuer']}
    </td>\n"""
        else:
            html_table += '    <td align="center" width="33%"></td>\n'
    html_table += "  </tr>\n"
html_table += "</table>"

new_content = content.replace(full_block, html_table)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Restored table layout for GitHub Markdown!")
