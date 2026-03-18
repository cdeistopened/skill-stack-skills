# Plugin Build History

Learnings from 3 completed plugin builds. Reference this when building a new plugin or improving an existing one.

## Completed Builds

| Plugin | Source | Skills | Frameworks | Indexes | Decomposition | Catalog |
|--------|--------|--------|------------|---------|---------------|---------|
| Ask Lenny | 303 podcast eps | 5 decision + 4 tutor + 1 utility + 1 router | 62 | 2 | Not saved | Yes (92 scored) |
| Ask KDP Kings | 175 eps + 37K book | 10 decision + 0 tutor + 0 utility + 1 router | 15 | 0 | 0 (book = scaffold) | No |
| Ask Huberman | 137 podcast eps | 6 decision + 4 tutor + 1 utility + 1 router | 47 | 3 | 5 (~50KB each) | No |

## File Locations

### Ask Lenny
- Plugin root: `wiki-projects/lennys-wiki/plugin/`
- Best decision skill: `skills/pmf-evaluator/SKILL.md`
- Best tutor skill: `skills/retention-workshop/SKILL.md`
- Best framework article: `references/frameworks/superhuman-pmf-engine.md`
- Router: `skills/ask-lenny/SKILL.md`

### Ask KDP Kings
- Plugin root: `wiki-projects/kdp-kings-wiki/plugin/`
- Best decision skill: `skills/niche-scout/SKILL.md`
- Best routing innovation: Stage map in `skills/ask-kdp/SKILL.md`
- Companion book: 37,876 words (unique asset)
- Biggest gap: Zero tutor skills, zero indexes

### Ask Huberman
- Plugin root: `wiki-projects/huberman-wiki/plugin/`
- Best decision skill: `skills/morning-routine-designer/SKILL.md`
- Best tutor skill: `skills/dopamine-masterclass/SKILL.md`
- Best framework article: `references/frameworks/physiological-sigh-protocol.md`
- Decomposition files: `references/decomposition-*.md` (5 files, ~50KB each)
- Indexes: `references/indexes/by-topic.md`, `by-protocol.md`, `by-supplement.md`

## Bugs Found and Fixed

1. **Phantom filenames in router** (Huberman, Lenny) — Router's framework search listed names that didn't match actual files. Fix: integrity check comparing referenced names vs actual files.

2. **Magnesium dosage inconsistency** (Huberman) — Decomposition found 145mg (precise Huberman number), but skill files said 300-400mg. Fix: always use decomposition files as source of truth for specific numbers.

3. **Duplicate framework articles** (Huberman) — Two agents covering overlapping domains produced `caffeine-timing-protocol` + `caffeine-adenosine-protocol` and `melatonin-position` + `melatonin-warning`. Fix: designate canonical names in indexes early, then merge + delete duplicates.

4. **Missing indexes** (KDP) — Router references `references/indexes/` but no indexes exist. Router can't do framework search. Fix: indexes are mandatory, not optional.

## Key Ratios (Use as Planning Guide)

| Metric | Lenny | KDP | Huberman | Target |
|--------|-------|-----|----------|--------|
| Frameworks per 100 episodes | 20 | 9 | 34 | 20-35 |
| Skills per plugin | 11 | 12 | 12 | 10-15 |
| Tutor : Decision ratio | 4:5 | 0:10 | 4:6 | 1:2 minimum |
| Index files | 2 | 0 | 3 | 2-4 |
| Decomp files saved | 0 | 0 | 5 | All |
