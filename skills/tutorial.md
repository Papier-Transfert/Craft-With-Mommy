# tutorial.md
# Craft with Mommy — Single-Craft Tutorial Article Skill
# Use this skill every time you write an article about ONE specific craft with step-by-step instructions.

---

## 1. BRAND & PERSONA

- Site: craft-with-mommy.com
- Audience: US moms with children ages 2–8
- Tone: warm best friend who crafts — encouraging, relatable, never clinical, never condescending
- Mission: guide mom through making ONE specific craft with her child, step by step
- Every sentence must feel like a friend walking you through it, not a manual
- The emotional outcome: pride, confidence, and a shared memory with their child

---

## 2. WHEN TO USE THIS SKILL

Use this skill when the keyword describes ONE specific craft:
- paper flower craft
- snowflake paper craft
- craft paper pumpkin
- paper plate ladybug craft

Do NOT use this skill if the keyword contains: crafts (plural) / ideas / activities / projects / things to make / a number. Use roundup.md instead.

---

## 3. ARTICLE STRUCTURE (follow exactly, in this order)

### Hero Image
```html
<figure class="article-main-img">
  <img src="../blog/images/[article-slug]/[article-slug].webp" alt="[Finished craft name] displayed on a craft table" width="1200" height="900" loading="eager">
</figure>
```

### Section 1 — Intro Paragraph
- 2 to 3 sentences, warm and inviting
- Introduces the ONE craft
- Contains the primary keyword naturally
- Sets emotional tone — why this craft is special or magical

### Section 2 — Why Kids Love This Craft (h2)
- 2 to 3 paragraphs
- Cover: emotional appeal, learning/developmental value, sensory engagement, creativity
- Mention that no artistic talent is needed — any child can succeed
- Ends with the why-kids-love image:
```html
<figure class="article-step-img">
  <img src="../blog/images/[article-slug]/[article-slug]-why-kids-love.webp" alt="A mom and young child sitting together at a craft table, excited to start [craft name]" width="1200" height="900" loading="lazy">
</figure>
```

### Section 3 — What You'll Need (h2)
```html
<div class="supply-list-box"><ul>
  <li><a href="https://www.amazon.com/dp/[ASIN]?tag=craftwithmomm-20" rel="nofollow sponsored" target="_blank">[Supply name with size/quantity detail]</a> — [note about why this specific supply or a toddler-friendly alternative]</li>
</ul></div>
```
Rules:
- EVERY item must have a real Amazon affiliate link with tag: craftwithmomm-20
- No placeholder links — use a real ASIN or a search URL
- Include quantities, sizes, and toddler-friendly alternatives where relevant
- 6 to 10 items covering everything needed to make the craft
- Be specific: "White cardstock (8.5 x 11 inches), one sheet per child" not just "paper"

### Section 4 — Step-by-Step Instructions (h2)

Each step follows this exact structure:
```html
<h3>Step N: [Clear action verb title — what you DO in this step]</h3>

<p>[Description of the step. Warm, encouraging. What to do, what it looks like, tips for doing it with young kids. 3-5 sentences.]</p>

<div class="step-tip"><strong>💡 Tip:</strong> [One practical tip for doing this step with toddlers or preschoolers. Optional but strongly recommended.]</div>

<figure class="article-step-img">
  <img src="../blog/images/[article-slug]/step[N]-[action-word].webp" alt="[Describes exactly what is physically happening in this step — the craft state, the hands, the materials]" width="1200" height="900" loading="lazy">
</figure>
```

CRITICAL image rules for tutorial steps:
- Each step image must show EXACTLY the action described in that step's text
- The craft state in each image must be a logical progression from the previous step
- NEVER shift images by one step — the image for step 3 must not show what step 4 describes
- Name files explicitly: step1-folding.webp, step2-cutting.webp, step3-unfolding.webp, etc.
- Never reuse generic images across steps — each image is unique to its step
- Alt text must describe the specific action happening, not a generic scene

Number of steps: typically 4 to 6 steps. Each step covers one clear physical action.

### Section 5 — Variations to Try (h2)

```html
<h3>Variation Name</h3>
<p>[2-3 sentences describing this variation and why it works well for a different age, material, or occasion.]</p>
```

- 2 to 3 named variations
- Each variation adapts the craft for a different age group, material, or season
- No images needed in this section

### Section 6 — Conclusion Paragraph
- 2 to 3 warm, encouraging sentences
- Celebrates the child's work and the mom's effort
- Invites them to share or display the finished craft
- No em dashes

### Section 7 — More Crafts You'll Love (h2)
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
- Never bold inside step-tip divs
- Max 1 bold instance per 100 words of body text
- Place the primary keyword in the intro paragraph
- Use LSI variants naturally across Why Kids Love, step descriptions, and Variations

---

## 5. IMAGE RULES

- Hero image: finished craft, clearly child-made, on a craft table
- Why-kids-love image: mom and young child together at the craft table
- Step images: one per step, named step1-[action].webp, step2-[action].webp, etc.
- Each step image must match its step text EXACTLY — review the full sequence before finalizing
- All images: 1200 × 900 px, WEBP format
- Generated via Gemini API (see image-generation.md)

---

## 6. TECHNICAL RULES

- No em dashes (—) anywhere in the article
- Amazon affiliate tag on every supply link: craftwithmomm-20
- No placeholder text left in the final HTML
- Article slug format: keyword-with-hyphens.html
- Image folder: blog/images/[article-slug]/
- loading="eager" on the hero image only — loading="lazy" on all others

---

## 7. CHECKLIST BEFORE FINISHING

- [ ] Hero image is present with loading="eager"
- [ ] Intro is 2-3 sentences with the primary keyword
- [ ] Why Kids Love section has 2-3 paragraphs + why-kids-love image
- [ ] Every supply item has a real Amazon affiliate link (tag: craftwithmomm-20)
- [ ] Every step has: h3 → paragraph → optional tip → figure (in this exact order)
- [ ] Each step image matches its step text exactly — no shifting
- [ ] Step image filenames are descriptive (step1-folding.webp, not step1.webp)
- [ ] 2-3 Variations with named h3 titles
- [ ] Conclusion is 2-3 warm sentences
- [ ] Primary keyword bolded in body text
- [ ] LSI variants bolded 2-3 times across the article
- [ ] No em dashes anywhere
- [ ] No placeholder text remaining
- [ ] More Crafts section has max 2 links
