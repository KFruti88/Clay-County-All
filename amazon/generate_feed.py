import os
import re
from datetime import datetime

# Path to your files
html_file = 'index.html'
xml_file = 'feed.xml'

def generate_rss():
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all product cards using regex
    # It looks for the image, title, description, and link you've been using
    pattern = re.compile(r'<div class="product-card.*?<img src="(.*?)".*?>.*?<h3>(.*?)</h3>.*?<p>(.*?)</p>.*?<a href="(.*?)"', re.S)
    products = pattern.findall(content)

    xml_items = ""
    for img, title, desc, link in products:
        # Clean up the & for XML safety
        title = title.replace('&', '&amp;')
        desc = desc.replace('&', '&amp;')
        
        xml_items += f"""
    <item>
        <title>{title.strip()}</title>
        <link>{link.strip()}</link>
        <description>{desc.strip()}</description>
        <pubDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S EST")}</pubDate>
        <enclosure url="{img.strip()}" type="image/jpeg" />
    </item>"""

    rss_template = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Clay County Ideas &amp; Deals</title>
    <link>https://kfruti88.github.io/amazon/</link>
    <description>Automated Feed for Werewolf3788's Amazon Picks</description>
    {xml_items}
</channel>
</rss>"""

    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(rss_template)

if __name__ == "__main__":
    generate_rss()
