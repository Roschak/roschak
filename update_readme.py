import re

# Read original README
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the table content
# The table starts at <table> and ends at </table>
table_match = re.search(r'<table>.*?</table>', content, re.DOTALL)
if not table_match:
    print("Table not found!")
    exit(1)

table_content = table_match.group(0)

# Extract each cell's data
# cell pattern: <td ...> <a href="(...)"> <img src="(...)" ... alt="(...)" /> </a> <br><br> <strong>(...)</strong> <br> (...) </td>
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

# CSS block
css_and_html = """<style>
  .cert-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    padding: 20px 0;
  }
  .cert-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
  }
  .cert-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 16px;
    border: 2px solid transparent;
    transition: border-color 0.4s ease-in-out;
    pointer-events: none;
  }
  .cert-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 15px 35px rgba(126, 231, 135, 0.2);
  }
  .cert-card:hover::before {
    border-color: rgba(126, 231, 135, 0.6);
  }
  .cert-image-container {
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 16px;
    aspect-ratio: 4/3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0,0,0,0.2);
  }
  .cert-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
  .cert-card:hover .cert-image-container img {
    transform: scale(1.08);
  }
  .cert-info {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: flex-end;
  }
  .cert-title {
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 6px;
    line-height: 1.4;
    color: #e6edf3;
  }
  .cert-issuer {
    font-size: 13px;
    color: #7d8590;
    font-weight: 500;
  }
  @media (max-width: 900px) {
    .cert-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  @media (max-width: 600px) {
    .cert-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

<div class="cert-grid">
"""

for cert in certs:
    css_and_html += f"""  <a href="{cert['href']}" class="cert-card" target="_blank" rel="noopener noreferrer">
    <div class="cert-image-container">
      <img src="{cert['img']}" alt="{cert['alt']}" loading="lazy" />
    </div>
    <div class="cert-info">
      <div class="cert-title">{cert['title']}</div>
      <div class="cert-issuer">{cert['issuer']}</div>
    </div>
  </a>
"""

css_and_html += "</div>"

new_content = content.replace(table_content, css_and_html)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully processed {len(certs)} certificates and updated README.md")
