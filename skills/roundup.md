# roundup.md
# Craft with Mommy — Roundup / Ideas Article Skill
# Use this skill every time you write a multi-idea article (20 crafts, 25 ideas, 15 activities, etc.)

---

## 1. BRAND & PERSONA

- Site: craft-with-mommy.com
- Audience: US moms with children ages 2–8
- Tone: warm best friend who crafts — encouraging, relatable, never clinical, never condescending
- Mission: help mom enjoy a low-stress, screen-free bonding moment with her kids through a simple DIY activity
- Every sentence must feel like advice from a friend, not instructions from a teacher
- The emotional outcome we want the reader to feel: joy, confidence, and connection

---

## 2. WHEN TO USE THIS SKILL

Use this skill when the keyword contains any of these signals:
- A number (20 crafts, 15 ideas, 25 activities)
- The words: crafts / ideas / activities / projects / things to make
- A plural promise in the title

Do NOT use this skill for a single-craft keyword. Use tutorial.md instead.

---

## 3. ARTICLE STRUCTURE (follow exactly, in this order)

### Section 1 — Intro
- 2 to 3 warm sentences only
- No "In this article" or "Today we're going to" language
- No list of what's coming
- Mention the primary keyword naturally in the first or second sentence
- Set a warm, excited tone — like you just sat down with a friend

### Section 2 — What You'll Need
```html
<div class="supply-list-box"><ul>
  <li><a href="https://www.amazon.com/dp/[ASIN]?tag=craftwithmomm-20" rel="nofollow sponsored" target="_blank">[Supply name]</a> — [one short note about why or what quantity]</li>
</ul></div>
```
Rules:
- 4 to 5 items maximum — broad basics that apply to most ideas in the list
- EVERY item must have a real Amazon affiliate link with tag: craftwithmomm-20
- No placeholder links — use a real ASIN or a search URL
- Do not list specialty items — only what you need for the majority of ideas

### Section 3 — Ideas (main body)

Use an h2 for the section title. Example: `<h2>20 Simple Paper Craft Ideas</h2>`

Each idea block MUST follow this exact order — no exceptions:

```html
<h3>N. Craft Name</h3>

<p>2 to 4 sentence description. Warm, encouraging tone. Bold the primary keyword or one LSI variant once if it fits naturally. No em dashes.</p>

<div class="idea-meta">
  <span class="badge">👶 Ages X+</span>
  <span class="badge">⏱ X min</span>
  <span class="badge">💧 Mess: Low/Medium/High</span>
</div>

<figure class="article-step-img">
  <img src="../blog/images/[article-slug]/[filename].webp" alt="[specific descriptive alt text for this craft]" width="1200" height="900" loading="lazy">
</figure>
```

CRITICAL rules for each idea block:
- idea-meta div ALWAYS comes before the figure — never after, never before the paragraph
- EVERY single idea must have an image — no exceptions, no ideas without images
- Age, time, and mess values must be realistic and appropriate for the craft
- Never use plain text for age/time/mess — always use the badge div with the exact HTML above
- Do not add any extra divs, wrappers, or classes not shown above
- The description paragraph must be written in the brand voice — warm, specific, encouraging

### Section 4 — Conclusion
- 1 to 2 warm sentences
- Encourage the mom to try it with her kids
- No bullet-point recap
- No summary of what was covered

### Section 5 — More Crafts You'll Love
```html
<h2>More Crafts You'll Love</h2>
<ul>
  <li><a href="/blog/[slug].html">[Article title]</a></li>
  <li><a href="/blog/[slug].html">[Article title]</a></li>
</ul>
```
- Max 2 internal links
- No intro paragraph before the list

---

## 4. SEO RULES

- Bold the primary keyword AND 2 to 3 LSI/related variants in body paragraph text only
- Never bold inside h3 headings
- Never bold inside idea-meta lines
- Max 1 bold instance per 100 words of body text
- Place the primary keyword in the first paragraph
- Use LSI variants naturally across different idea descriptions — do not repeat the same bold phrase

---

## 5. IMAGE RULES

- EVERY idea must have its own image — 100% coverage, no exceptions
- Images are generated via Gemini API after the HTML is written (see image-generation.md)
- Use [IMAGE_PENDING] as a temporary src placeholder when writing HTML before images are generated
- Each image must show the specific finished craft for that idea — not a generic craft table scene
- Alt text must describe the exact craft shown in that image
- File naming: use a short descriptive slug (e.g. paper-strip-caterpillar.webp)
- All images: 1200 × 900 px, WEBP format

---

## 6. TECHNICAL RULES

- No em dashes (—) anywhere in the article — use commas, periods, or "and" instead
- Amazon affiliate tag on every supply link: craftwithmomm-20
- No placeholder text left in the final HTML — no [YOUR NAME], no [LINK HERE], no [IMAGE]
- Article slug format: keyword-with-hyphens.html
- Image folder: blog/images/[article-slug]/
- Hero image src: ../blog/images/[article-slug]/[article-slug].webp
- loading="eager" on the hero image only — loading="lazy" on all others

---

## 7. CHECKLIST BEFORE FINISHING

Before considering the article complete, verify every item:

- [ ] Intro is 2-3 sentences, warm, no tutorial language
- [ ] Supply box has 4-5 items, every item has a real Amazon affiliate link
- [ ] Every idea has: h3 → paragraph → idea-meta → figure (in this exact order)
- [ ] Every idea has an image (0 ideas without images)
- [ ] No idea has two idea-meta divs
- [ ] No idea has zero idea-meta divs
- [ ] Age/time/mess values are realistic
- [ ] Primary keyword is bolded at least once in body text
- [ ] LSI variants are bolded 2-3 times across the article
- [ ] No em dashes anywhere
- [ ] No placeholder text remaining
- [ ] Conclusion is 1-2 sentences
- [ ] More Crafts section has max 2 links, no intro paragraph
- [ ] All image alts are descriptive and specific
