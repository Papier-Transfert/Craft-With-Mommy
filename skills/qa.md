*Run a final quality-assurance audit on completed Craft with Mommy blog articles.*

# Purpose

This skill performs the final QA check for Craft with Mommy blog articles.

It does not choose the keyword and does not replace the writing skills. It audits the completed article before it is considered finished.

Do not consider the article complete until all checks pass. If any issue is found, fix it before finalizing the article.

# Article Type Detection

First, determine which article type you are auditing:

## Tutorial article

A tutorial article teaches one specific craft step by step.

## Roundup article

A roundup article presents multiple craft ideas in one article.

Use the correct checklist based on the actual article type.

# Common QA Checks

Verify all of the following:

- the primary keyword came from `/tools/unused-keywords.txt`
- the keyword was not invented or reused from memory
- once the article is fully completed, the keyword is removed from `/tools/unused-keywords.txt`
- once the article is fully completed, the keyword is added to `/tools/used-keywords.txt`
- the article type was chosen correctly
- the article uses the correct skill structure for its type
- the primary keyword appears in the permalink
- the permalink is short, clear, and ideally under 75 characters
- the search-result title includes the primary keyword clearly
- the `<title>` tag is under 60 characters
- the primary keyword appears in the first 50 characters of the title
- the meta description is present and under 155 characters (Google truncates around 155)
- a canonical URL tag is present: `<link rel="canonical" href="https://www.craft-with-mommy.com/blog/[slug].html">`
- all six Open Graph tags are present: og:type, og:title, og:description, og:url, og:site_name, og:image
- og:title matches the article `<title>` tag
- og:description matches the meta description
- og:image points to the hero image of the article
- the article uses clean semantic HTML
- there are no placeholders left in the final article
- no em dashes appear anywhere in the article
- bold keyword usage is natural and not excessive
- the article contains between 3 and 8 emojis total
- every affiliate link uses the tag `craftwithmomm-20`
- every affiliate link uses the `/dp/ASIN` format, not a generic search URL
- ASIN accuracy cannot be verified during QA — it depends on the writing skill's ASIN verification rule having been followed during article creation. If there is reason to believe an ASIN was not verified via WebSearch at write time, flag it for manual review.
- tutorials use HowTo JSON-LD schema; roundups use Article JSON-LD schema — QA fails if the schema type is missing or wrong for the article type
- image filenames are descriptive and SEO-friendly
- image alt text is descriptive and useful
- final images are WEBP
- final images are 1200 × 900
- the article has been assigned to the correct collections
- the homepage carousel at `/index.html` has been updated with the new article
- the new article appears as the first `<article class="craft-card">` inside
  `<div class="crafts-track" id="craftsTrack">`
- the carousel contains exactly 9 cards — not 8, not 10
- the oldest card (formerly the 9th) has been removed
- QA fails if the carousel was not updated, or if the count is not exactly 9

- no affiliate link contains an ASIN that was recalled from memory without
  being verified in this session via WebSearch
- every /dp/ASIN link has been confirmed: the product page title and category
  match the intended supply item
- QA fails if any affiliate link is broken, irrelevant, mismatched, or points
  to a product in the wrong category
- QA fails if a supply item has no affiliate link only because verification
  was skipped — either verify or omit, never guess

  ### Image Border and Framing QA Checks

- Fail if any article image shows visible white or transparent padding around the photo
- Fail if any image looks letterboxed or pillarboxed
- Fail if the actual photo content does not reach the rounded corners visually
- Fail if an image looks like a smaller picture placed on a blank canvas instead of filling the frame naturally
- If this happens, crop or regenerate the image before finalizing the article


# Tutorial-Specific Checks

If the article is a tutorial, verify all of the following:

- breadcrumb is present and stays on one line
- mobile breadcrumb title truncates with an ellipsis if too long
- top pills include category, age, time, and messiness in the correct order
- the title is the only `<h1>` on the page
- publication date is present
- hero image matches the finished craft
- intro is short, warm, and natural
- "Why Kids Love This Craft" section is present and useful
- secondary image matches that section
- "What You'll Need" includes all real required materials
- there is a short intro sentence before the supply list in "What You'll Need"
- affiliate links are helpful and not forced
- the tutorial includes between 5 and 10 steps
- there is a short intro paragraph under "Step-by-Step Instructions" before Step 1
- tips appear selectively, not in every step
- each step is physically logical and easy to follow
- each step image matches exactly the corresponding step
- step images are not shifted by one step
- the craft remains visually consistent across all step images
- "Variations to Try" is present and each variation meaningfully adapts the craft (different age, material, theme, or technique — not just a different color). If any variation is weak, it must be removed rather than kept.
- "Final Thoughts" is warm and encouraging
- "More Crafts You'll Love" contains exactly 2 relevant internal links
- every internal link in "More Crafts You'll Love" points to a slug listed in `/tools/used-keywords.txt`
- the article ends on a warm, encouraging note
- article word count is between 1200 and 2900 words

# Roundup-Specific Checks

If the article is a roundup, verify all of the following:

- breadcrumb is present and stays on one line
- mobile breadcrumb title truncates with an ellipsis if too long
- only the category pill appears at the top
- no global age, time, or messiness pills appear at the top
- the title is the only `<h1>` on the page
- publication date is present
- hero image matches the roundup theme accurately
- intro is short, warm, and natural
- "What You'll Need" includes useful broad supplies for most of the ideas
- there is a short intro sentence under "What You'll Need"
- the article includes between 10 and 30 ideas
- if the title promises a specific number, the article contains exactly that number of ideas
- every idea includes an h3 title, a useful paragraph, realistic badges, and an image
- every image appears after the badges, not before
- every idea image matches its exact idea
- "Final Thoughts" is present
- "More Crafts You'll Love" contains exactly 2 relevant internal links
- every internal link in "More Crafts You'll Love" points to a slug listed in `/tools/used-keywords.txt`
- the article ends on a warm, friendly note
- article word count is between 1200 and 2900 words

  ### Listing and Collection QA Checks

- Fail if the new article does not appear on `/blog/`
- Fail if the new article does not appear on its main craft collection page
- Fail if the article should appear in a seasonal or thematic collection but is missing there
- Verify that the article card uses the correct title, slug, hero image, category, date, and metadata
- Fail if the homepage carousel at `/index.html` was not updated
- Fail if the new article is not the first `<article class="craft-card">` inside `<div class="crafts-track" id="craftsTrack">`
- Fail if the carousel contains more or fewer than exactly 9 cards
- Do not finalize or commit until discoverability is confirmed

# Output Behavior

After the QA pass:

- if all checks pass, the article can be considered complete
- if any important issue is found, fix it before finalizing the article
- do not mark an article as done if core structure, SEO, image, affiliate, or keyword-queue rules are still broken

*This skill is intentionally simple. Its job is to audit the finished article, catch mistakes, and block final completion until everything is correct.*
