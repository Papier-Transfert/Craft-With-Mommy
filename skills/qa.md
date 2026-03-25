# qa.md
# Craft with Mommy — Quality Assurance Skill
# Run this skill on every article before committing and pushing.
# An article that fails any item below must be fixed before it goes live.

---

## HOW TO RUN THIS QA

1. Read the article HTML file from top to bottom
2. Check every item in this list
3. Fix every failure before moving on
4. Only commit when all items pass

---

## SECTION A — STRUCTURE

### A1. Article type is correct
- If the keyword is a single craft → the article uses tutorial structure (Why Kids Love, What You'll Need, Step-by-Step, Variations)
- If the keyword promises multiple ideas → the article uses roundup structure (intro, supplies, numbered ideas, conclusion)
- The two structures must never be mixed

### A2. All required sections are present
**Tutorial:** Intro → Why Kids Love → What You'll Need → Step-by-Step Instructions → Variations to Try → Conclusion → More Crafts You'll Love

**Roundup:** Intro → What You'll Need → [N] Numbered Ideas → Conclusion → More Crafts You'll Love

### A3. Section order is correct
Verify the sections appear in the exact order listed above. No sections are out of place or missing.

### A4. More Crafts You'll Love
- Maximum 2 internal links
- No intro paragraph before the list
- Both links point to real existing articles on the site

---

## SECTION B — IDEA BLOCKS (roundup only)

### B1. Every idea has exactly one idea-meta div
- No idea has zero idea-meta divs
- No idea has two idea-meta divs

### B2. Idea block order is correct for every idea
Order must be: `<h3>` → `<p>` → `<div class="idea-meta">` → `<figure>`
- idea-meta comes AFTER the paragraph
- figure comes AFTER idea-meta
- Nothing comes between idea-meta and figure except whitespace

### B3. Every idea has an image
- Count the ideas (h3 tags with numbers)
- Count the article-step-img figures in the body
- Every idea must have exactly one figure
- Zero ideas without an image is the target

### B4. Badge format is correct
Each idea-meta div must contain exactly 3 badges in this order:
```html
<span class="badge">👶 Ages X+</span>
<span class="badge">⏱ X min</span>
<span class="badge">💧 Mess: Low/Medium/High</span>
```
- No plain text age/time/mess lines (no `<p><em>Age: 3+ | Time: 10 min</em></p>`)
- No missing badges
- No extra badges

---

## SECTION C — STEPS (tutorial only)

### C1. Every step has an image
- Count the h3 step headings
- Count the article-step-img figures
- Every step must have exactly one figure

### C2. Step images match their step text
- Read each step's text, then look at its image src and alt
- The alt text must describe the action happening in that step
- The image must not show what the next or previous step describes
- Step image filenames must be descriptive: step1-folding.webp, not step1.webp

### C3. Step image sequence is logical
- Step 1 image shows the starting action
- Each subsequent step image shows the craft in a more advanced state
- No visual regression (step 3 image cannot look earlier in the process than step 2)

---

## SECTION D — SUPPLIES

### D1. Every supply item has an Amazon affiliate link
- Open the supply-list-box
- Every `<li>` must contain an `<a>` tag
- Every `<a>` href must contain: `tag=craftwithmomm-20`
- No placeholder links ([LINK HERE], amazon.com without an ASIN, etc.)

### D2. No placeholder ASINs
- Links must use real ASINs (format: /dp/B00XXXXXXX) or real search URLs
- Do not leave template ASINs like B00000000 or XXXXXXXXXX

---

## SECTION E — SEO & COPY

### E1. Primary keyword is present and bolded
- The primary keyword appears in the intro paragraph
- It is wrapped in `<strong>` tags at least once in body text
- It is NOT bolded inside an h2, h3, or idea-meta div

### E2. LSI variants are bolded
- 2 to 3 related keyword variants are bolded across the article body
- Max 1 bold instance per 100 words

### E3. No em dashes
- Search the file for — (em dash character)
- Zero instances allowed anywhere in the article

### E4. No placeholder text
Search for and confirm zero instances of:
- [Your Name]
- [LINK HERE]
- [IMAGE]
- [ROUNDUP_IMAGE_PLACEHOLDER]
- [ADD IMAGE]
- ASIN in all caps
- Any text inside square brackets [ ]

### E5. Tone is correct
- Read the intro and conclusion out loud mentally
- Does it sound like a warm friend talking to another mom?
- Is there any clinical, instructional, or robotic language?
- Are there any sentences that feel generic or copy-paste-ish?

---

## SECTION F — IMAGES

### F1. Hero image is present
- The article-main-img figure is present near the top
- src points to ../blog/images/[article-slug]/[article-slug].webp
- loading="eager" (not lazy)

### F2. All body images exist on disk
- Every src in an article-step-img figure must point to a file that exists in /var/www/craft-with-mommy/blog/images/[article-slug]/
- No broken image paths

### F3. All images are the correct format and size
- All image files are .webp
- All images are 1200 × 900 px

### F4. Alt texts are descriptive and specific
- No alt text is generic ("image of a craft")
- No alt text is empty
- Each alt describes the specific craft or action shown in that image

---

## SECTION G — TECHNICAL

### G1. HTML is valid
- No unclosed tags
- No nested `<a>` inside `<a>`
- No `<figure>` outside of the article body

### G2. Meta tags are present and correct
- `<title>` — contains the article title and "Craft with Mommy"
- `<meta name="description">` — 150-160 characters, contains the primary keyword
- `<link rel="canonical">` — points to the correct URL
- `<meta property="og:title">` — present
- `<meta property="og:image">` — points to the hero image

### G3. JSON-LD schema is correct
- Roundup articles: `"@type": "Article"`
- Tutorial articles: `"@type": "HowTo"`
- No placeholder values inside the schema

### G4. Nav is correct
- Full navigation is present
- The article's collection is highlighted correctly in the nav if applicable

---

## QA PASS CRITERIA

The article passes QA when:
- Every item above is checked
- Every failure has been fixed
- A final read-through confirms the article reads naturally from top to bottom

Only after passing QA:
→ Update the keyword queue
→ Commit and push
