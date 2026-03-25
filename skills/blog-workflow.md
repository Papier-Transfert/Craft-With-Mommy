*Run the Craft with Mommy daily blog workflow.*

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
9. Commit all new and changed files:
   ```
   git add blog/[slug].html blog/images/[slug]/ blog/index.html blog/[collection].html index.html tools/unused-keywords.txt tools/used-keywords.txt
   git commit -m "Add [article type]: [keyword]"
   ```
10. Push to GitHub: `git push origin main` — Vercel auto-deploys from GitHub. The article goes live after ~60 seconds.
11. Verify deployment: After pushing, wait ~90 seconds then use WebFetch to confirm the article URL returns HTTP 200 (not 404). Fetch `https://www.craft-with-mommy.com/blog/[slug].html` and confirm the page loads with the correct title.
12. Verify listings: Also fetch `https://www.craft-with-mommy.com/` and confirm the new article appears as the first card in the Latest Crafts carousel. Fetch `https://www.craft-with-mommy.com/blog/` and confirm the article appears at the top of the listing.
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
- all four listing updates were done (blog listing, collection page, seasonal page if applicable, homepage carousel)
- only then was the keyword moved from unused to used
- all files were committed and pushed to GitHub
- deployment confirmed live via WebFetch (article URL returns 200, not 404)
- article appears in homepage carousel and blog listing on the live site
- live URL reported to user

### Post-Publish Listing Update Rules

After creating a new article, update all four of the following. The article is not considered fully published until all four are done.

**1. Blog listing page**
Add the new article card to `/blog/index.html` immediately after `<!-- ARTICLE_CARDS_START -->`.

**2. Main craft collection page**
Add the new article card to the correct craft collection page (e.g., `/blog/paper-crafts.html`) immediately after `<!-- ARTICLE_CARDS_START -->`.

**3. Seasonal or thematic collection page**
If the article belongs to a seasonal or thematic collection (e.g., Christmas Crafts, Animal Crafts), add the card to that page too, immediately after `<!-- ARTICLE_CARDS_START -->`.

**4. Homepage carousel**
Update the "Latest Crafts" carousel at `/index.html` - this is the root homepage file, NOT `/blog/index.html`.

The carousel is inside this section:
```
<!-- LATEST CRAFTS -->
<div class="crafts-track" id="craftsTrack">
```

Rules:
- The carousel must always contain exactly 9 articles at all times.
- Insert the new article as the FIRST `<article class="craft-card">` immediately after the opening `<div class="crafts-track" id="craftsTrack">` line.
- Delete the LAST `<article class="craft-card">` element (which becomes the 10th after insertion) so the total stays at exactly 9.
- Confirm the carousel contains exactly 9 cards after the edit.

Carousel card format:
```html
<article class="craft-card">
  <a href="blog/[slug].html" style="display:block;color:inherit;">
    <div class="craft-thumb" style="background: linear-gradient(135deg, #[color1], #[color2]);">
      <img src="blog/images/[slug]/[hero-image-filename].webp"
           alt="[full article title]"
           style="width:100%;height:100%;object-fit:cover;" loading="lazy">
    </div>
    <div class="craft-body">
      <div class="craft-tag">[collection emoji] [Collection Name]</div>
      <h3 class="craft-title">[full article title]</h3>
      <div class="craft-meta"><span>⏱ 15 min</span><span>⭐ Beginner</span></div>
    </div>
  </a>
</article>
```

- Choose a distinct pastel gradient for the new card that is not already used by another card currently in the carousel.
- Do not change anything else in `/index.html`. Do not touch the carousel CSS, JavaScript, dots, or any other section of the page.
