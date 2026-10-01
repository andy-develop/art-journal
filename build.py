#!/usr/bin/env python3
import os
import re
from html.parser import HTMLParser
from pathlib import Path

# 原站路径
SRC_DIR = "/Users/andy/DoubaoWork/chats/2026-10-01/new-chat-1/maltm-mirror/www.maltm.com"
# 输出路径
OUT_DIR = "/Users/andy/DoubaoWork/chats/2026-10-01/new-chat-1/art-website"

# 瑞士网格模板
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — art</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --bg: #FFFFFF;
    --ink: #0A0A0A;
    --ink-2: #555555;
    --ink-3: #999999;
    --accent: #FF4D00;
    --line: #E5E5E5;
  }}
  body {{
    background: var(--bg);
    color: var(--ink);
    font-family: 'Inter', -apple-system, sans-serif;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}
  .topbar {{
    border-bottom: 1px solid var(--line);
    padding: 0.75rem 3rem;
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: var(--ink-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .header {{
    padding: 2rem 3rem;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 3rem;
    border-bottom: 1px solid var(--line);
  }}
  .logo {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    text-decoration: none;
    color: var(--ink);
  }}
  .nav {{
    display: flex;
    gap: 2rem;
    list-style: none;
  }}
  .nav a {{
    color: var(--ink-2);
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}
  .nav a:hover {{ color: var(--accent); }}
  .article-header {{
    padding: 4rem 3rem;
    max-width: 900px;
    margin: 0 auto;
  }}
  .article-cat {{
    display: inline-block;
    background: var(--accent);
    color: white;
    padding: 0.25rem 0.75rem;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
  }}
  .article-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1.75rem, 3vw, 2.75rem);
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
  }}
  .article-meta {{
    display: flex;
    gap: 2rem;
    font-size: 0.75rem;
    color: var(--ink-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .article-hero {{
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    aspect-ratio: 16/9;
    overflow: hidden;
    background: #f0f0f0;
  }}
  .article-hero img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}
  .article-content {{
    max-width: 800px;
    margin: 0 auto;
    padding: 4rem 3rem;
  }}
  .article-content p {{
    margin-bottom: 1.5rem;
    color: var(--ink-2);
    font-size: 1rem;
    line-height: 1.8;
  }}
  .article-content img {{
    width: 100%;
    margin: 2rem 0;
  }}
  .article-nav {{
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 3rem 4rem;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--line);
  }}
  .article-nav a {{
    color: var(--ink);
    text-decoration: none;
    font-size: 0.85rem;
  }}
  .article-nav a:hover {{ color: var(--accent); }}
  footer {{
    padding: 2rem 3rem;
    text-align: center;
    font-size: 0.7rem;
    color: var(--ink-3);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-top: 1px solid var(--line);
  }}
  @media (max-width: 900px) {{
    .header {{ grid-template-columns: 1fr; gap: 1rem; padding: 1.5rem; }}
    .nav {{ display: none; }}
    .topbar {{ padding: 0.5rem 1.5rem; }}
    .article-header {{ padding: 2rem 1.5rem; }}
    .article-content {{ padding: 2rem 1.5rem; }}
    .article-nav {{ padding: 1.5rem; flex-direction: column; gap: 1rem; }}
  }}
</style>
</head>
<body>

<div class="topbar">
  <span>Independent Journal</span>
  <span>Design · Art · Culture</span>
  <span>Est. 2017</span>
</div>

<header class="header">
  <a href="{back_url}index.html" class="logo">art/</a>
  <ul class="nav">
    <li><a href="{back_url}#design">Design</a></li>
    <li><a href="{back_url}#art">Art</a></li>
    <li><a href="{back_url}#fashion">Fashion</a></li>
    <li><a href="{back_url}#photo">Photography</a></li>
    <li><a href="{back_url}#music">Music</a></li>
  </ul>
  <a href="{back_url}index.html" style="font-size: 0.75rem; color: var(--ink-2); text-decoration: none;">← Back</a>
</header>

<article>
  <header class="article-header">
    <span class="article-cat">{category}</span>
    <h1 class="article-title">{title}</h1>
    <div class="article-meta">
      <span>{date}</span>
    </div>
  </header>

  <div class="article-hero">
    <img src="{hero_image}" alt="{title}">
  </div>

  <div class="article-content">
    {content}
  </div>

  <nav class="article-nav">
    <a href="{back_url}index.html">← All Stories</a>
    <a href="#">Next Story →</a>
  </nav>
</article>

<footer>
  © 2025 art journal · Design · Art · Culture
</footer>

</body>
</html>
"""


def extract_article_info(html_path):
    """从原站HTML中提取文章信息"""
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # 提取标题
    title_match = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>.*?</h3>', html, re.DOTALL)
    if not title_match:
        title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Untitled"
    title = re.sub(r'<[^>]+>', '', title).strip()
    title = title.split('|')[0].strip()
    
    # 提取分类
    cat_match = re.search(r'class="labelBox[^"]*">(.*?)</div>', html, re.DOTALL)
    category = "Design"
    if cat_match:
        cats = re.findall(r'<a[^>]*>(.*?)</a>', cat_match.group(1))
        if cats:
            category = cats[0].strip()
    
    # 提取日期
    date_match = re.search(r'<time>(.*?)</time>', html)
    date = date_match.group(1).strip() if date_match else ""
    
    # 提取主图
    img_match = re.search(r'data-original="([^"]+)"', html)
    hero_image = img_match.group(1) if img_match else ""
    # 转换为相对路径
    if hero_image.startswith('/'):
        hero_image = '../..' + hero_image
    elif not hero_image.startswith('http'):
        hero_image = '../../' + hero_image
    
    # 提取正文内容（简单提取p标签）
    content_parts = []
    # 尝试找正文区域
    content_match = re.search(r'<div class="article[^"]*">(.*?)</div>\s*<!--', html, re.DOTALL)
    if not content_match:
        content_match = re.search(r'<div class="content[^"]*">(.*?)</div>\s*<footer', html, re.DOTALL)
    
    if content_match:
        content_html = content_match.group(1)
        # 提取p标签
        ps = re.findall(r'<p[^>]*>(.*?)</p>', content_html, re.DOTALL)
        for p in ps[:10]:  # 取前10段
            p_clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(p_clean) > 20:  # 过滤太短的
                content_parts.append(f"<p>{p_clean}</p>")
    
    # 如果没提取到正文，用占位
    if not content_parts:
        content_parts.append("<p>这是一篇关于设计、艺术与文化的深度文章。更多内容正在整理中。</p>")
    
    return {
        'title': title,
        'category': category,
        'date': date,
        'hero_image': hero_image,
        'content': '\n    '.join(content_parts)
    }


def generate_article_page(article_slug, info, out_dir):
    """生成单篇文章页面"""
    article_dir = os.path.join(out_dir, 'articles', article_slug)
    os.makedirs(article_dir, exist_ok=True)
    
    # 计算返回首页的相对路径
    back_url = '../../'
    
    html = TEMPLATE.format(
        title=info['title'],
        category=info['category'],
        date=info['date'],
        hero_image=info['hero_image'],
        content=info['content'],
        back_url=back_url
    )
    
    with open(os.path.join(article_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    return article_slug, info['title']


def main():
    src_path = Path(SRC_DIR)
    out_path = Path(OUT_DIR)
    
    # 获取所有文章目录（排除content/category/wp-includes/feed）
    articles = []
    for item in src_path.iterdir():
        if item.is_dir() and item.name not in ['content', 'category', 'wp-includes', 'feed']:
            index_file = item / 'index.html'
            if index_file.exists():
                articles.append(item)
    
    print(f"找到 {len(articles)} 篇文章")
    
    # 处理每篇文章
    processed = []
    for i, article_dir in enumerate(articles):
        slug = article_dir.name
        index_file = article_dir / 'index.html'
        
        try:
            info = extract_article_info(str(index_file))
            result = generate_article_page(slug, info, str(out_path))
            processed.append(result)
            print(f"[{i+1}/{len(articles)}] ✅ {slug} - {info['title'][:30]}")
        except Exception as e:
            print(f"[{i+1}/{len(articles)}] ❌ {slug} - {e}")
    
    print(f"\n完成！成功处理 {len(processed)} 篇文章")
    return processed


if __name__ == '__main__':
    main()
