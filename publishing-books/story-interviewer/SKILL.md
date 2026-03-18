# Story Interviewer Skill

Interview mode for extracting personal stories, finding hidden themes, and connecting them to book narratives.

---

## Purpose

Draw out **credibility-building stories** from the author's life that:
- Demonstrate lived experience with the book's concepts
- Reveal hidden themes the author may not consciously recognize
- Provide concrete, sensory-rich material for the manuscript
- Build authority through vulnerability and specificity

---

## The Interview Flow

### Phase 1: Story Extraction

**Opening prompt:**
> "Tell me about a time when [book theme] showed up in your life. Don't worry about making it sound good - just tell me what happened."

**Follow-up probes:**
- "What were you feeling in that moment?"
- "What did you see, hear, smell?"
- "Who else was there? What did they say?"
- "What happened right before that? Right after?"
- "What's the detail you almost didn't mention?"

**The hidden gem question:**
> "What's a story you've never told anyone - or almost never tell - that relates to this?"

### Phase 2: Theme Discovery

After the story is told, reflect back:

1. **Surface theme**: What the story is obviously about
2. **Hidden theme**: What it reveals about the author's deeper values/struggles
3. **Universal theme**: How it connects to the reader's experience
4. **Book connection**: Which chapter/concept this story supports

**Theme-finding questions:**
- "Why do you think this story stuck with you?"
- "What would your younger self think about how this turned out?"
- "If this story had a title, what would it be?"
- "What's the lesson you learned that you haven't said out loud yet?"

### Phase 3: Story Documentation

Output each story as a **Narrative Snippet** (see format below).

---

## Narrative Snippet Format

```markdown
# [Story Title]

**Book:** Benedict Challenge / JFK 50
**Chapter connection:** [Which chapter this supports]
**Theme:** [One-line theme]
**Credibility angle:** [What authority this establishes]

---

## The Story (Raw)

[Verbatim or lightly edited version of what Charlie told]

---

## Sensory Details

- **Visual:** [What was seen]
- **Auditory:** [What was heard]
- **Physical:** [Body sensations, environment]
- **Emotional:** [Internal state]

---

## Key Quotes

> "[Direct quote from Charlie during interview]"

---

## Hidden Themes Identified

1. **[Theme 1]:** [How it shows up in this story]
2. **[Theme 2]:** [How it connects to book thesis]

---

## Manuscript Integration Notes

- **Where to use:** [Specific chapter/section]
- **How to frame:** [Suggested lead-in]
- **Caution:** [What to avoid when telling this publicly]

---

**Tags:** #story #[book] #[chapter] #[theme]
**Captured:** [Date]
```

---

## Story Prompts by Book

### Benedict Challenge Stories

| Theme | Prompt |
|-------|--------|
| Fasting breakthrough | "Tell me about a time fasting changed something for you" |
| Discipline failure | "When did you completely fail at a discipline you set?" |
| Physical transformation | "Describe a moment you felt different in your body" |
| Spiritual clarity | "When did fasting lead to an insight you didn't expect?" |
| Family/community | "How has this practice affected your family?" |

### JFK 50 Stories

| Theme | Prompt |
|-------|--------|
| Endurance moment | "Tell me about hitting a wall and pushing through" |
| Physical limits | "When did your body surprise you?" |
| Mental game | "What mind trick got you through something hard?" |
| Training story | "Describe a training day that changed your approach" |
| The why | "Why does this challenge matter to you personally?" |

---

## Interview Session Checklist

Before ending a story interview session:

- [ ] At least one raw story captured
- [ ] Sensory details extracted (see/hear/feel)
- [ ] Hidden theme identified
- [ ] Chapter connection mapped
- [ ] Story saved to `stories/` folder with proper naming

---

## File Organization

```
Book/
├── stories/
│   ├── benedict-fasting-breakthrough-001.md
│   ├── benedict-discipline-failure-001.md
│   └── jfk50-endurance-moment-001.md
```

---

## Usage

Start an interview session:
```
/interview [book] [theme]
```

Example:
```
/interview benedict fasting-breakthrough
/interview jfk50 endurance
```

Or just say: "Interview me about stories for the Benedict book"

---

*Philosophy: Your stories are your moat. Generic advice is in the training data. Your specific experiences - told with sensory detail and emotional honesty - are what no one else can write.*
