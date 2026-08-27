import re

# Read original pristine README
with open('README_original.md', 'r', encoding='utf-16') as f:
    orig_content = f.read()

table_match = re.search(r'<table>.*?</table>', orig_content, re.DOTALL)
if not table_match:
    print("Table not found in original!")
    exit(1)
table_content = table_match.group(0)

# Extract each cell's data
td_pattern = re.compile(
    r'<td.*?>\s*<a href="([^"]+)">(.*?)<img\s+src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/>(.*?)</a>\s*<br><br>\s*<strong>(.*?)</strong>\s*<br>\s*(.*?)\s*</td>',
    re.DOTALL
)

certs = []
for match in td_pattern.finditer(table_content):
    href = match.group(1).strip()
    img_src = match.group(3).strip()
    alt_text = match.group(4).strip()
    title = match.group(6).strip()
    issuer = match.group(7).strip()
    certs.append({
        'href': href,
        'img': img_src,
        'alt': alt_text,
        'title': title,
        'issuer': issuer
    })

print(f"Found {len(certs)} certs")

# Build 5-column HTML table
html_table = "<table>\n"
for i in range(0, len(certs), 5):
    html_table += "  <tr>\n"
    for j in range(5):
        if i + j < len(certs):
            cert = certs[i + j]
            # Set width to 20% for 5 columns
            html_table += f"""    <td align="center" width="20%">
      <a href="{cert['href']}">
        <img src="{cert['img']}" width="100%" alt="{cert['alt']}" />
      </a>
      <br><br>
      <strong>{cert['title']}</strong>
      <br>
      {cert['issuer']}
    </td>\n"""
        else:
            html_table += '    <td align="center" width="20%"></td>\n'
    html_table += "  </tr>\n"
html_table += "</table>"

# Now we must safely insert this into README.md
with open('README.md', 'r', encoding='utf-8') as f:
    current_content = f.read()

# Let's replace everything between `<p align="center">\n  <i>Certifications, courses, and achievements — all verified certificates</i>\n</p>`
# and `<br>\n\n<p align="center">\n  <i>📜 Continuously learning`
start_marker = "<i>Certifications, courses, and achievements — all verified certificates</i>\n</p>"
end_marker = "<br>\n\n<p align=\"center\">\n  <i>📜 Continuously learning"

start_idx = current_content.find(start_marker)
end_idx = current_content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found in current README.md!")
    exit(1)

start_idx += len(start_marker)

new_content = current_content[:start_idx] + "\n\n" + html_table + "\n\n" + current_content[end_idx:]

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully built 5-column table and updated README.md")
