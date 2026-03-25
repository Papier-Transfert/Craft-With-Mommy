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
- the meta description is present and under 300 characters
- the article uses clean semantic HTML
- there are no placeholders left in the final article
- no em dashes appear anywhere
- bold keyword usage is natural and not excessive
- affiliate links are real and use the tag `craftwithmomm-20`
- affiliate links point to real, specific Amazon product pages
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
- affiliate links are helpful and not forced
- the tutorial includes between 5 and 10 steps
- there is a short intro paragraph under "Step-by-Step Instructions" before Step 1
- tips appear selectively, not in every step
- each step is physically logical and easy to follow
- each step image matches exactly the corresponding step
- step images are not shifted by one step
- the craft remains visually consistent across all step images
- "Variations to Try" is present and useful
- "Final Thoughts" is warm and encouraging
- "More Crafts You'll Love" contains exactly 2 relevant internal links

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
- the article ends on a warm, friendly note

  ### Listing and Collection QA Checks

- Fail if the new article does not appear on `/blog/`
- Fail if the new article does not appear on its main craft collection page
- Fail if the article should appear in a seasonal or thematic collection but is missing there
- Verify that the article card uses the correct title, slug, hero image, category, date, and metadata
- Do not finalize or commit until discoverability is confirmed

# Output Behavior

After the QA pass:

- if all checks pass, the article can be considered complete
- if any important issue is found, fix it before finalizing the article
- do not mark an article as done if core structure, SEO, image, affiliate, or keyword-queue rules are still broken

*This skill is intentionally simple. Its job is to audit the finished article, catch mistakes, and block final completion until everything is correct.*
