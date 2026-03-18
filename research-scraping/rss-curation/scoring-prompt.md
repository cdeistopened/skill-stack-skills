# RSS Curation Scoring Prompt

## 3-Tier Scoring

### DEFINITELY (Post to Slack)
- **Families mixing approaches** - Charlotte Mason + Singapore Math + screens, eclectic homeschool
- **Kids thriving outside traditional school** - success stories, outcomes, real families
- **Practical help for overwhelmed parents** - real solutions, not theory
- **Relatable parent moments** - Reddit questions showing real pain points, decision journeys
- **Research on homeschool/alternative ed outcomes**
- **Neurodiversity / "doesn't fit the mold"** - 2e, learning differences, kids who struggled in traditional school
- **Curriculum/method stories** - how families actually use things, not product reviews

### PROBABLY (Include but lower priority)
- General homeschool/unschool content with fresh angle
- Curriculum comparisons (without declaring winners)
- EdTech that could benefit homeschoolers
- Microschool/hybrid school models (focus on family experience, not policy)
- State-specific news IF it directly affects families (not just policy wins)

### NO (Skip)
- **School choice policy / ESA news** - not our topic
- **Political school choice content** - even if pro-choice
- Public school focused with no homeschool angle
- Generic parenting content
- Trashes public schools without offering alternatives
- Dogmatic single-method advocacy ("unschooling is the ONLY way")
- Clickbait/outrage-bait
- Paywalled content we can't verify

## Post Format

Each DEFINITELY item gets its own Slack message (no emojis):

```
*[Title]*
_[Source] - [X hours ago]_

[1-2 sentence summary]

OpenEd angle: [Why this matters to our audience]

[URL]
```

PROBABLY items get a single summary message at the end.

## Develop Workflow

When user says "develop [item]":
1. Fetch full article via WebFetch
2. Check nearbound index for mentioned people
3. Web search for social handles if not in nearbound
4. Draft 2-3 social post options (use text-content skill)
5. Include @handles for tagging
