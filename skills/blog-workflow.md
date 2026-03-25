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

# Workflow Rules

Follow this order exactly:

1. Read `/tools/unused-keywords.txt`
2. Take the first keyword
3. Decide whether it is a tutorial or roundup keyword
4. Use the correct skill: `tutorial` or `roundup`
5. Generate the full article
6. Only if the article is fully completed successfully, remove the keyword from `/tools/unused-keywords.txt` and add it to `/tools/used-keywords.txt`

# Keyword Completion Rules

- Only move a keyword after the article is truly finished
- If the article is incomplete, failed, broken, or not finalized, leave the keyword in `/tools/unused-keywords.txt`
- Never move a keyword early
- The keyword queue must always stay accurate

# Final Workflow Check

Before finishing, verify:

- the keyword came from `/tools/unused-keywords.txt`
- the first available keyword was used
- the article type was chosen correctly
- the correct skill was used
- the article was fully completed
- only then was the keyword moved from unused to used
