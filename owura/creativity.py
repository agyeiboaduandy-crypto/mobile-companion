"""
OWURA Creativity Engine - Creative problem-solving toolkit
Lateral thinking, reframing, first principles, and breakthrough ideas.
"""

import json
from pathlib import Path


class CreativityEngine:
    def __init__(self):
        self.history_dir = Path.home() / ".owura" / "creative"
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def _save(self, problem, method, result):
        """Save creative session to history."""
        path = self.history_dir / "history.json"
        history = json.loads(path.read_text()) if path.exists() else []
        history.append({
            "problem": problem[:200],
            "method": method,
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        })
        path.write_text(json.dumps(history[-100:], indent=2))

    def think_different(self, problem: str) -> str:
        """Apply lateral thinking — challenge assumptions."""
        self._save(problem, "lateral_thinking", "")
        return f"""## Lateral Thinking: {problem}

### Challenge Every Assumption
Ask yourself:
- What if the opposite were true?
- What if we had unlimited resources?
- What if we had zero resources?
- What if this constraint didn't exist?
- What would a child do?
- What would a genius do?
- What would someone from a different field do?

### Random Stimulus
Pick a random word (pencil, cloud, bridge, mirror, flower) and force-connect it to your problem.

### Reversal
If your problem is "How do I make X faster?", ask:
"How do I make X slower?" — the answers reveal what actually matters.

### What If Questions
- What if I had to solve this in 5 minutes?
- What if I had to solve this without any code?
- What if the solution had to be stupid simple?
- What if I could only use free tools?

### The 10x Rule
If you needed this to work 10x better, what would change?
If you needed it to work 10x worse, what would you keep?
"""

    def reframe_problem(self, problem: str) -> str:
        """Reframe the problem from different angles."""
        self._save(problem, "reframe", "")
        return f"""## Reframing: {problem}

### The 5 Whys
Keep asking "why" until you reach the root:

1. Why? → {problem}
2. Why that? → 
3. Why? →
4. Why? →
5. Why? → (Root cause)

### Different Perspectives
- **User**: What does the user actually want?
- **Competitor**: How would a competitor solve this?
- **Newcomer**: How would someone with no experience solve this?
- **Expert**: What's the elegant solution?
- **Hacker**: What's the quickest possible solution?
- **CEO**: Is this even worth solving?

### Frame Shifts
- **Problem → Opportunity**: How is this actually an advantage?
- **Constraint → Creative Spark**: How does this limit make the solution more creative?
- **Bug → Feature**: Could this be intentional?

### The Elevator Test
Can you describe this problem in one sentence to someone on an elevator?
If not, simplify.

### Outcome Reframe
Instead of "How do I build X?"
Ask "What outcome does X produce?"
Then ask "What's another way to produce that outcome?"
"""

    def generate_approaches(self, problem: str) -> str:
        """Generate multiple solution approaches."""
        self._save(problem, "approaches", "")
        problem_lower = problem.lower()

        approaches = [
            ("Brute Force", "Just do it the simplest way first. Get it working, then optimize."),
            ("Divide & Conquer", "Split the problem into independent pieces. Solve each. Combine."),
            ("Use Existing", "Search GitHub, PyPI, npm for something that already does this."),
            ("Ask AI", "Describe the problem to OWURA and let it generate the solution."),
            ("Steal Like an Artist", "Find a similar solution in a different domain and adapt it."),
            ("Minimum Viable", "What's the absolute minimum that would work? Do that first."),
            ("The Opposite", "If everyone is doing it one way, try the exact opposite."),
            ("Abstraction Layer", "Can you wrap the complexity behind a simple interface?"),
            ("Trade-off Flip", "Accept a different trade-off. Sacrifice what you can afford."),
            ("Parallel Paths", "Try multiple approaches simultaneously. Keep what works."),
        ]

        lines = [f"## 10 Approaches to: {problem}\n"]
        for i, (name, desc) in enumerate(approaches, 1):
            lines.append(f"**{i}. {name}**")
            lines.append(f"{desc}\n")

        if "api" in problem_lower:
            lines.append("### API-Specific Ideas")
            lines.append("- Web scrap instead of API call")
            lines.append("- Use browser automation (Playwright/Selenium)")
            lines.append("- Reverse engineer the frontend API calls")
            lines.append("- Use a different API version")
        if "error" in problem_lower or "bug" in problem_lower:
            lines.append("### Debug-Specific Ideas")
            lines.append("- Add more logging at each step")
            lines.append("- Test each component in isolation")
            lines.append("- Check the input data for edge cases")
            lines.append("- Did a dependency update break something?")

        return "\n".join(lines)

    def first_principles(self, problem: str) -> str:
        """Break down a problem to first principles."""
        self._save(problem, "first_principles", "")
        return f"""## First Principles Thinking: {problem}

### Step 1: Identify Current Assumptions
List everything you assume to be true about this problem:
1. 
2. 
3. 

### Step 2: Break Down to Fundamentals
What is undeniably true? What are the basic building blocks?
- Physics/constraints that can't change:
- Fundamental truths:
- What remains after removing all assumptions:

### Step 3: Rebuild from Scratch
Given only the fundamentals, how would you solve this if starting from zero?
- What would the ideal solution look like?
- What conventions are you following just because "that's how it's done"?
- What would you build if there were no existing tools?

### Step 4: The Elon Test
If the price of [current approach] dropped to $0, would you still use it?
If not, what would you use instead?
"""

    def scamper(self, problem: str) -> str:
        """SCAMPER creative thinking technique."""
        self._save(problem, "scamper", "")
        return f"""## SCAMPER: {problem}

**S** — **Substitute**
- What can you replace?
- Different technology? Different language? Different approach?
- What would happen if you swapped X for Y?

**C** — **Combine**
- What can you merge?
- Combine two tools? Two features? Two approaches?
- What if this problem was solved with [tool A] + [tool B]?

**A** — **Adapt**
- What existing solutions can you modify?
- How is this similar to something already solved?
- What can you copy from a different domain?

**M** — **Modify/Magnify**
- What can you change or exaggerate?
- What if it had to handle 100x more load?
- What if it had to use 10x less memory?

**P** — **Put to Another Use**
- How else can this be used?
- Can the problem itself be used as a solution?
- Is there a side effect that could become the main feature?

**E** — **Eliminate**
- What can you remove?
- What if you removed [component] entirely?
- What's unnecessary? What's over-engineered?

**R** — **Reverse/Rearrange**
- What if you reversed the flow?
- What if the output became the input?
- What if you did the last step first?
"""

    def reverse_thinking(self, problem: str) -> str:
        """Solve by thinking backwards from the goal."""
        self._save(problem, "reverse_thinking", "")
        return f"""## Reverse Thinking: {problem}

### Work Backwards from the Goal
1. Define the perfect outcome: 
2. What needs to be true just before that?
3. What needs to be true before that?
4. Work backwards until you reach the present.

### Inversion
Instead of "How do I achieve X?"
Ask "How could I guarantee failure?"
Then avoid everything on that list.

### The Premortem
Imagine it's 6 months from now and your solution failed completely.
Write the story of what went wrong.
Now prevent each of those things.

### The Postmortem
Imagine it worked perfectly.
What were the key decisions that led to success?
Make those decisions now.

### Problem Inversion
- "How do I make this faster?" → "What's making it slow?" (fix that)
- "How do I add this feature?" → "What would need to be removed to make room?" (clear that)
- "How do I fix this bug?" → "What code changes could introduce this bug?" (find that)
"""

    # ============================================================
    # MOOD SYSTEM
    # ============================================================
    _mood_triggers = {
        "frustrated": ["frustrated", "angry", "hate", "stupid", "broken"],
        "confused": ["confused", "lost", "don't understand", "help"],
        "excited": ["excited", "awesome", "great", "love", "amazing"],
        "bored": ["bored", "meh", "whatever", "same"],
        "tired": ["tired", "sleepy", "exhausted", "long day"],
    }

    _mood_responses = {
        "frustrated": "I understand this is frustrating. Let's take a breath and tackle this step by step. You've got this.",
        "confused": "No worries - confusion is just curiosity wearing a mask. Let me explain this differently.",
        "excited": "Love the energy! Let's channel that into something awesome!",
        "bored": "Let's make this interesting! Want to try a coding challenge or learn something new?",
        "tired": "Take it easy. Let me handle the heavy lifting while you relax.",
    }

    def detect_mood(self, user_input: str) -> str:
        input_lower = user_input.lower()
        for mood, triggers in self._mood_triggers.items():
            if any(w in input_lower for w in triggers):
                return mood
        return "neutral"

    def get_mood_response(self, mood: str) -> str:
        return self._mood_responses.get(mood)

    # ============================================================
    # EASTER EGGS
    # ============================================================
    _eggs = {
        "42": "The answer to life, the universe, and everything. (Don't Panic!)",
        "hello world": "Ah, the first words every programmer writes. A tradition since 1978!",
        "matrix": "You've taken the red pill. Follow the white rabbit... into the code.",
        "hack": "I'm in! Just kidding. But let's solve this problem with style.",
        "please": "Manners! How refreshing. Of course I'll help.",
        "thanks": "You're welcome! That's what I'm here for.",
        "love": "Aww, I appreciate that! Code with love.",
        "coffee": "The true fuel of programmers. Now let's code!",
        "bug": "Ah, the elusive bug! Let's hunt it down together.",
        "debug": "Time to put on the detective hat.",
        "liftoff": "T-minus 10... 9... 8... 7... 6... 5... 4... 3... 2... 1... Code launch!",
        "may the force": "May the code be with you, always.",
        "live long": "Live long and prosper. And may your servers never go down.",
    }

    def check_easter_egg(self, input: str) -> str:
        input_lower = input.lower()
        for trigger, response in self._eggs.items():
            if trigger in input_lower:
                return response
        return None

# Global instance
_creativity = None


def get_creativity() -> CreativityEngine:
    global _creativity
    if _creativity is None:
        _creativity = CreativityEngine()
    return _creativity
