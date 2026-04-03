---
name: blog-workflow
description: Use when running the Craft with Mommy daily blog publishing workflow. Triggers include any request to run the blog workflow, publish the next article, or process the keyword queue. This skill orchestrates keyword selection, article type routing, and post-publish listing updates. Do not use for writing or auditing articles directly.
---

# Purpose

This skill manages the daily blog workflow for Craft with Mommy.

It does not write the article itself. It decides which article skill to use and manages the keyword queue correctly.

# Run Schedule

This workflow is intended to run 2 times per day:

- 08:00
- 18:00

Important: The scheduling itself must be handled by the external automation system. This skill only defines the expected workflow when it runs.

# Keyword Queue Files

Use these files as the single source of truth:

- `/tools/unused-keywords.txt`
- `/tools/used-keywords.txt`

# Keyword Selection Rules

- Always read `/tools/unused-keywords.txt` first
- Always take the first available keyword from the top of the file
- Do not invent a keyword
- Do not choose a keyword from memory
- Do not skip ahead unless explicitly instructed
- Never reuse a keyword already listed in `/tools/used-keywords.txt`

# Article Type Decision Rules

After reading the keyword, decide whether it should become:

- a tutorial article
- a roundup / ideas article

## Use tutorial when:

- the keyword clearly refers to one specific craft
- the article should teach one project step by step

Examples:

- paper chain craft
- paper turkey craft
- tissue paper flower craft

## Use roundup when:

- the keyword clearly refers to a list of multiple craft ideas
- the keyword suggests a theme, collection, or topic with many ideas

Examples:

- paper arts and crafts
- top 10 paper christmas crafts
- paper halloween crafts
- paper mache crafts

## When in doubt

If a keyword could be either a tutorial or a roundup, default to **tutorial**.

A keyword is only a roundup if it contains a clear multi-idea signal (e.g., "top 10", "25 ideas", "crafts for kids", "paper crafts ideas"). If the keyword sounds like it could be one specific craft, choose tutorial.

# Workflow Rules

Follow this order exactly:

1. Read `/tools/unused-keywords.txt`
2. Take the first keyword
3. Decide whether it is a tutorial or roundup keyword
4. Derive the article slug from the keyword (e.g., `top 10 paper christmas crafts` → `top-10-paper-christmas-crafts.html`)
5. Check whether `/blog/[slug].html` already exists. If the file already exists, do not write the article again. Instead, move the keyword from `/tools/unused-keywords.txt` to `/tools/used-keywords.txt` and stop.
6. Use the correct skill: `tutorial` or `roundup`
7. Generate the full article
8. Only if the article is fully completed successfully, remove the keyword from `/tools/unused-keywords.txt` and add it to `/tools/used-keywords.txt`
9. Update sitemap.xml — run this Python snippet to regenerate it with all current articles:
   ```python
   import os, re
   BASE_URL = "https://www.craft-with-mommy.com"
   BLOG_DIR = "/var/www/craft-with-mommy/blog"
   COLLECTION_PAGES = {"index.html","paper-crafts.html","paper-plate-crafts.html","handprint-crafts.html","recycled-crafts.html","animal-crafts.html","spring-crafts.html","summer-crafts.html","fall-crafts.html","winter-crafts.html","christmas-crafts.html"}
   SKIP_PAGES = {"crafts.html","seasons.html"}
   DATE_PAT = re.compile(r'Published on (January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})')
   MONTH_MAP = {"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06","July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}
   def get_date(f):
       try:
           m = DATE_PAT.search(open(f,encoding='utf-8').read(20000))
           return f"{m.group(3)}-{MONTH_MAP[m.group(1)]}-{m.group(2).zfill(2)}" if m else "2026-03-20"
       except: return "2026-03-20"
   lines = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">','','  <!-- Static pages -->','  <url><loc>https://www.craft-with-mommy.com/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>','  <url><loc>https://www.craft-with-mommy.com/blog/</loc><changefreq>daily</changefreq><priority>0.9</priority></url>','  <url><loc>https://www.craft-with-mommy.com/about.html</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>','  <url><loc>https://www.craft-with-mommy.com/legal.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>','  <url><loc>https://www.craft-with-mommy.com/privacy.html</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>','','  <!-- Collection pages -->']
   for fname in sorted(os.listdir(BLOG_DIR)):
       if fname.endswith('.html') and fname in COLLECTION_PAGES and fname != "index.html":
           lines.append(f'  <url><loc>{BASE_URL}/blog/{fname}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
   lines += ['','  <!-- Article pages -->']
   for fname in sorted(os.listdir(BLOG_DIR)):
       if fname.endswith('.html') and fname not in COLLECTION_PAGES and fname not in SKIP_PAGES:
           d = get_date(os.path.join(BLOG_DIR,fname))
           lines += [f'  <url>',f'    <loc>{BASE_URL}/blog/{fname}</loc>',f'    <lastmod>{d}</lastmod>',f'    <changefreq>monthly</changefreq>',f'    <priority>0.7</priority>',f'  </url>']
   lines.append('</urlset>')
   open('/var/www/craft-with-mommy/sitemap.xml','w').write('\n'.join(lines))
   print("sitemap.xml updated")
   ```
10. Commit all new and changed files:
   ```
   git add blog/[slug].html blog/images/[slug]/ blog/index.html blog/[collection].html tools/unused-keywords.txt tools/used-keywords.txt sitemap.xml
   git commit -m "Add [article type]: [keyword]"
   ```
11. Push to GitHub: `git push origin main` — Vercel auto-deploys from GitHub. The article goes live after ~60 seconds.
12. Verify deployment: After pushing, wait ~90 seconds then use WebFetch to confirm the article URL returns HTTP 200 (not 404). Fetch `https://www.craft-with-mommy.com/blog/[slug].html` and confirm the page loads with the correct title.
13. Report to user: Once all three checks pass, send the user: (a) confirmation the deployment is live, (b) the live article URL. Do not report success until WebFetch confirms the page loads correctly.

# Keyword Completion Rules

- Only move a keyword after the article is truly finished
- If the article is incomplete, failed, broken, or not finalized, leave the keyword in `/tools/unused-keywords.txt`
- Never move a keyword early
- The keyword queue must always stay accurate

# Final Workflow Check

Before finishing, verify:

- the keyword came from `/tools/unused-keywords.txt`
- the first available keyword was used
- the slug was checked for collision before writing
- the article type was chosen correctly
- the correct skill was used
- the article was fully completed
- all three listing updates were done (blog listing, collection page, seasonal page if applicable)
- only then was the keyword moved from unused to used
- sitemap.xml was regenerated and included in the commit
- all files were committed and pushed to GitHub
- deployment confirmed live via WebFetch (article URL returns 200, not 404)
- article appears in the blog listing on the live site
- live URL reported to user

### Post-Publish Listing Update Rules

After creating a new article, update all three of the following. The article is not considered fully published until all three are done.

**1. Blog listing page**
Add the new article card to `/blog/index.html` immediately after `<!-- ARTICLE_CARDS_START -->`.

**2. Main craft collection page**
Add the new article card to the correct craft collection page (e.g., `/blog/paper-crafts.html`) immediately after `<!-- ARTICLE_CARDS_START -->`.

**3. Seasonal or thematic collection page**
If the article belongs to a seasonal or thematic collection (e.g., Christmas Crafts, Animal Crafts), add the card to that page too, immediately after `<!-- ARTICLE_CARDS_START -->`.

Collection page card format (use this exact structure for all three listing updates above):
```html
<article class="blog-card">
  <a href="/blog/[slug].html">
    <div class="blog-card-thumb">
      <img src="../blog/images/[slug]/[hero-image-filename].webp" alt="[full article title]" loading="lazy">
    </div>
    <div class="blog-card-body">
      <div class="blog-card-tag">[collection emoji] [Collection Name]</div>
      <h3 class="blog-card-title">[full article title]</h3>
      <div class="blog-card-meta">
        <span>📅 [Publication Date]</span>
      </div>
    </div>
  </a>
</article>
```

