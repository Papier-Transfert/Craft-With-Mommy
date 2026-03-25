# blog-workflow.md
# Craft with Mommy — Daily Blog Workflow Skill
# This skill manages the full process from keyword to published article.
# Run this skill first, before roundup.md or tutorial.md.

---

## 1. DAILY SCHEDULE

- Article 1: published at 8:00 AM
- Article 2: published at 6:00 PM
- 2 articles per day, every day

---

## 2. STEP 1 — RECEIVE THE KEYWORD

The user provides a keyword. Example:
```
Keyword: paper chain craft
```

If no keyword is provided, read the next unused keyword from:
`/var/www/craft-with-mommy/tools/unused-keywords.txt`

Pick the first keyword in the list that has not been used yet.

---

## 3. STEP 2 — IDENTIFY THE ARTICLE TYPE

Read the keyword and decide which article type applies:

**→ Use roundup.md if the keyword contains:**
- A number (20 crafts, 15 ideas, 25 activities)
- The words: crafts / ideas / activities / projects / things to make
- Any plural promise of multiple items

**→ Use tutorial.md if the keyword describes:**
- One specific craft (paper flower craft, snowflake paper craft, paper plate ladybug)
- A single object or technique with no plural promise

State your decision out loud before proceeding. Example:
```
Keyword: paper chain craft
Type: TUTORIAL (one specific craft)
Reading: skills/tutorial.md
```

---

## 4. STEP 3 — READ THE SKILL FILE

Before writing a single word of the article, read the appropriate skill file:
- Roundup → read `/var/www/craft-with-mommy/skills/roundup.md`
- Tutorial → read `/var/www/craft-with-mommy/skills/tutorial.md`

Do not rely on memory. Read the file fresh every time.

---

## 5. STEP 4 — GENERATE THE ARTICLE HTML

Apply the skill exactly. Write the full HTML file including:
- All meta tags (title, description, canonical, og:*)
- JSON-LD schema (Article for roundup, HowTo for tutorial)
- Full nav (copy structure from an existing article)
- Full article body following the skill structure
- No placeholder text anywhere in the final file

Save the file to:
```
/var/www/craft-with-mommy/blog/[article-slug].html
```

---

## 6. STEP 5 — GENERATE THE IMAGES

After the HTML is written, generate all images via the Gemini API.
Read `/var/www/craft-with-mommy/skills/image-generation.md` for the full image generation process.

Do not skip this step. No article is complete without its images.

---

## 7. STEP 6 — RUN THE QA CHECK

Before committing, read and apply `/var/www/craft-with-mommy/skills/qa.md`.

The QA check is mandatory. Do not commit an article that has not passed QA.

---

## 8. STEP 7 — UPDATE THE KEYWORD QUEUE

After the article passes QA:

1. Move the keyword from `unused-keywords.txt` to `used-keywords.txt`
2. Add the entry to `used-keywords.txt` in this format:
   ```
   [keyword] | [collection] | [article-slug].html
   ```
3. Mark the keyword as `"used": true` in `keywords_queue.json`

---

## 9. STEP 8 — COMMIT AND PUSH

Commit all changes with a clear message:
```
git add blog/[article-slug].html blog/images/[article-slug]/
git commit -m "Publish [Article Title] ([article type]: roundup or tutorial)"
git push origin main
```

Confirm the push succeeded before considering the article done.

---

## 10. FULL WORKFLOW SUMMARY

```
User gives keyword
       ↓
Identify type (roundup or tutorial)
       ↓
Read skill file (roundup.md or tutorial.md)
       ↓
Write full HTML article
       ↓
Generate images (image-generation.md)
       ↓
Run QA check (qa.md)
       ↓
Update keyword queue
       ↓
Commit and push
       ↓
DONE
```

---

## 11. RULES THAT APPLY TO BOTH ARTICLE TYPES

These rules are always active, regardless of article type:

- No em dashes (—) anywhere
- Amazon affiliate tag: craftwithmomm-20 on every supply link
- Bold primary keyword + 2-3 LSI variants in body text only (never in headings)
- Max 1 bold per 100 words
- No placeholder text in the final file
- Every image: 1200 × 900 px, WEBP format, loading="lazy" (except hero: loading="eager")
- Internal links only go to existing published articles on the site
- The article must be coherent from top to bottom — re-read it before committing

---

## 12. SITE REFERENCE

- Domain: craft-with-mommy.com
- Repo: /var/www/craft-with-mommy/
- Blog articles: /var/www/craft-with-mommy/blog/
- Images: /var/www/craft-with-mommy/blog/images/[article-slug]/
- Tools and scripts: /var/www/craft-with-mommy/tools/
- Keyword queue: /var/www/craft-with-mommy/tools/keywords_queue.json
- Used keywords: /var/www/craft-with-mommy/tools/used-keywords.txt
- Unused keywords: /var/www/craft-with-mommy/tools/unused-keywords.txt
- Skills: /var/www/craft-with-mommy/skills/
