"""
OWURA Creativity Engine - Makes OWURA feel alive and unique
Storytelling, metaphors, gamification, and more.
"""

import random
import json
from pathlib import Path
from datetime import datetime

class CreativityEngine:
    def __init__(self):
        self.mood = "neutral"
        self.session_jokes = []
    
    # ============================================================
    # 1. STORYTELLING MODE - Explain as stories
    # ============================================================
    def tell_story(self, concept: str) -> str:
        """Explain a coding concept as a story."""
        
        stories = {
            "recursion": """
**The Story of the Infinite Mirror**

Once upon a time, there was a function called `factorial`.
It had one job: to count how many ways you could arrange things.

But factorial had a secret - it was lazy. Instead of counting itself,
it would call a smaller version of itself and say "you figure it out."

"5! = 5 * 4!" it would say.
And 4! would say "4! = 4 * 3!"
And 3! would say "3! = 3 * 2!"
And 2! would say "2! = 2 * 1!"
And 1! would say "1! = 1" (the base case, the end of the story)

Then the answers would bubble back up like a stack of plates,
each one multiplying what came back.

And so 5! became 5 * 24 = 120.

The moral? Sometimes the best way to solve a big problem is to
make it smaller and ask someone else (yourself) to handle it.

**The End** ðŸŽ­
""",
            "async": """
**The Story of the Busy Chef**

Chef Async worked at a busy restaurant.
Instead of waiting for water to boil (blocking),
she would start the water, then immediately chop vegetables.

"I'll come back to the water when it's ready," she said.

This is `async/await` - the art of not waiting.

While `await fetch('api')` is running,
the chef can do other things.

When the data comes back, the chef returns to continue the recipe.

The result? A meal prepared in half the time.

**The End** ðŸ³
""",
            "api": """
**The Story of the Restaurant**

You (the client) sit at a table.
You don't go into the kitchen (server) yourself.
You don't tell the chef how to cook (implementation).

You just tell the waiter (API) what you want:
"I'll have the user data, please."

The waiter takes your request to the kitchen.
The kitchen prepares it.
The waiter brings it back.

You don't need to know how it's cooked.
You just enjoy the result.

That's an API - a polite middleman between you and the magic.

**The End** ðŸ½ï¸
""",
            "database": """
**The Story of the Library**

Imagine a library with millions of books (data).
You could walk through every shelf (full table scan),
but that would take forever.

Instead, the librarian (database engine) has a card catalog (index).
Looking for "Python Recipes"? 
The librarian checks the index, finds the exact shelf, 
and brings you the book in seconds.

Databases are just very fast, very organized libraries.

**The End** ðŸ“š
""",
            "git": """
**The Story of the Time Traveler**

Git is a time machine for your code.

Made a mistake? Travel back to yesterday's version.
Want to try something crazy? Create a parallel universe (branch).
Love the result? Merge the universes together.

Every commit is a snapshot in time.
Every branch is a "what if?"
Every merge is "best of both worlds."

You are the time traveler. Git is your machine.

**The End** â°
""",
        }
        
        concept_lower = concept.lower()
        
        for key, story in stories.items():
            if key in concept_lower:
                return story
        
        return f"""
**The Story of {concept}**

Once upon a time, there was a problem called `{concept}`.
It seemed impossible at first.

But then, someone had an idea...
They broke it into smaller pieces.
Each piece was simple.
Together, they were powerful.

The code ran. The bug was fixed. The feature worked.

And the developer lived happily ever after.

**The End** âœ¨
"""
    
    # ============================================================
    # 2. METAPHOR GENERATOR - Explain with metaphors
    # ============================================================
    def generate_metaphor(self, concept: str) -> str:
        """Generate a metaphor for a coding concept."""
        
        metaphors = {
            "variable": "A variable is a labeled box. You put something in, write the label, and can find it later.",
            "function": "A function is a recipe. You give it ingredients (inputs), it follows steps, and gives you a dish (output).",
            "loop": "A loop is a broken record. It keeps playing the same line until you tell it to stop.",
            "array": "An array is a filing cabinet. Each drawer has a number, and you can pull out exactly what you need.",
            "class": "A class is a blueprint. It describes what a house should look like, but isn't a house itself.",
            "object": "An object is a house built from the blueprint. It has real walls, real rooms, real life.",
            "API": "An API is a waiter. You order, they fetch, you eat. You never see the kitchen.",
            "database": "A database is a library with the world's fastest librarian.",
            "server": "A server is a very patient robot. It waits for requests, all day, every day.",
            "bug": "A bug is a gremlin. Small, annoying, and sometimes hiding in the most obvious place.",
            "debug": "Debugging is detective work. Look for clues, follow the trail, catch the culprit.",
            "refactor": "Refactoring is spring cleaning. Same house, just organized better.",
            "recursion": "Recursion is looking in a mirror that's facing another mirror. Infinity, but with a base case.",
            "async": "Async is multitasking. Start the laundry, cook dinner, do homework - all at once.",
            "callback": "A callback is a promise. 'When you're done, call me back.'",
            "closure": "A closure is a backpack. It carries its environment wherever it goes.",
            "promise": "A promise is a IOU. 'I'll get back to you with the result.'",
            "tuple": "A tuple is a locked list. Once created, it can never change.",
            "dictionary": "A dictionary is a word-to-meaning map. Look up the word, get the meaning.",
        }
        
        concept_lower = concept.lower()
        
        for key, metaphor in metaphors.items():
            if key in concept_lower:
                return f"**Metaphor for {key}:**\n\n{metaphor}"
        
        return f"**Metaphor for {concept}:**\n\nHmm, let me think... {concept} is like... a puzzle piece that fits into the bigger picture of your code."
    
    # ============================================================
    # 3. CREATIVE CODE NAMING
    # ============================================================
    def generate_names(self, purpose: str) -> str:
        """Generate creative variable/function names."""
        
        prefixes = ["get", "fetch", "load", "find", "calculate", "process", "transform", "build", "create", "generate"]
        suffixes = ["data", "info", "result", "output", "response", "value", "item", "element", "node", "entry"]
        
        purpose_words = purpose.lower().split()
        
        names = []
        
        # Direct naming
        names.append("_".join(purpose_words))
        names.append(purpose_words[0] if purpose_words else "data")
        
        # Prefix + purpose
        for prefix in random.sample(prefixes, 3):
            names.append(f"{prefix}_{purpose_words[0] if purpose_words else 'data'}")
        
        # Purpose + suffix
        for suffix in random.sample(suffixes, 3):
            names.append(f"{purpose_words[0] if purpose_words else 'data'}_{suffix}")
        
        # Creative combinations
        creative = [
            f"the_{purpose_words[0]}_machine",
            f"process_{purpose_words[0]}_magic",
            f"ultimate_{purpose_words[0]}",
            f"super_{purpose_words[0]}_transformer",
        ]
        names.extend(random.sample(creative, 2))
        
        lines = [f"## Creative Names for: {purpose}\n"]
        lines.append("**Professional:**")
        for name in names[:4]:
            lines.append(f"  - `{name}`")
        
        lines.append("\n**Fun:**")
        for name in names[4:]:
            lines.append(f"  - `{name}`")
        
        return "\n".join(lines)
    
    # ============================================================
    # 4. CODE POETRY
    # ============================================================
    def code_poem(self, language: str = "python") -> str:
        """Generate a poetic code snippet."""
        
        poems = {
            "python": '''
```python
# A Poem in Python

def dream(of_worlds):
    """We dream in functions,
    sleeping in loops,
    waking in variables,
    living in objects."""
    
    for star in universe:
        if star.is_bright:
            yield light(star)
    
    return hope  # Always return hope

class Life:
    def __init__(self):
        self.purpose = "to learn"
        self.journey = []
    
    def live(self):
        while self.purpose:
            experience = self.encounter()
            self.journey.append(experience)
            self.grow(experience)
    
    def __repr__(self):
        return f"A story of {len(self.journey)} moments"
```
''',
            "javascript": '''
```javascript
// A Poem in JavaScript

const universe = () => {
    const stars = Array.from({length: Infinity});
    
    return stars.map((_, i) => ({
        id: i,
        light: `Star ${i}`,
        dream: () => `Shining in the void`
    }));
};

// We are all just async functions,
// waiting for our promises to resolve,
// catching errors along the way,
// finally{} reaching our end.

async function life() {
    try {
        const meaning = await findPurpose();
        return meaning;
    } catch (confusion) {
        return learn(confusion);
    } finally {
        console.log("It was worth it");
    }
}
```
''',
        }
        
        return poems.get(language, poems["python"])
    
    # ============================================================
    # 5. GAMIFICATION - Coding challenges
    # ============================================================
    def get_challenge(self, difficulty: str = "easy") -> str:
        """Get a random coding challenge."""
        
        challenges = {
            "easy": [
                {"name": "FizzBuzz Classic", "task": "Print 1-100, but multiples of 3 say 'Fizz', 5 say 'Buzz', both say 'FizzBuzz'", "hint": "Use modulo operator %"},
                {"name": "Reverse String", "task": "Write a function that reverses a string", "hint": "Try slicing [::-1]"},
                {"name": "Find Maximum", "task": "Find the largest number in a list without using max()", "hint": "Loop and compare"},
                {"name": "Count Vowels", "task": "Count how many vowels are in a string", "hint": "Check each character"},
            ],
            "medium": [
                {"name": "Palindrome Checker", "task": "Check if a string reads the same backwards", "hint": "Compare string with its reverse"},
                {"name": "Anagram Detector", "task": "Check if two strings are anagrams", "hint": "Sort both and compare"},
                {"name": "Matrix Transpose", "task": "Transpose a 2D matrix (swap rows and columns)", "hint": "Use zip()"},
                {"name": "Binary Search", "task": "Implement binary search on a sorted list", "hint": "Divide and conquer"},
            ],
            "hard": [
                {"name": "Maze Solver", "task": "Find a path through a 2D maze from start to end", "hint": "Try recursion or BFS"},
                {"name": "LRU Cache", "task": "Implement a Least Recently Used cache", "hint": "Use OrderedDict or linked list"},
                {"name": "HTTP Server", "task": "Build a basic HTTP server from scratch", "hint": "Use sockets"},
                {"name": "Regex Engine", "task": "Implement basic regex matching", "hint": "Start with . and * only"},
            ],
        }
        
        difficulty = difficulty.lower() if difficulty.lower() in challenges else "easy"
        challenge = random.choice(challenges[difficulty])
        
        return f"""## Coding Challenge ({difficulty.title()})

**Name:** {challenge['name']}

**Task:** {challenge['task']}

**Hint:** {challenge['hint']}

**Difficulty:** {difficulty.title()}

Type your solution when ready, or say "hint" for more help!
"""
    
    # ============================================================
    # 6. WISDOM GENERATOR
    # ============================================================
    def get_wisdom(self) -> str:
        """Get programming wisdom."""
        
        wisdoms = [
            (""The best code is no code at all."", "Jeff Atwood"),
            (""First, solve the problem. Then, write the code."", "John Johnson"),
            (""Any fool can write code that a computer can understand. Good programmers write code that humans can understand."", "Martin Fowler"),
            (""Programs must be written for people to read, and only incidentally for machines to execute."", "Harold Abelson"),
            (""Simplicity is prerequisite for reliability."", "Edsger W. Dijkstra"),
            (""The most dangerous phrase is: We've always done it this way."", "Grace Hopper"),
            (""Talk is cheap. Show me the code."", "Linus Torvalds"),
            (""Premature optimization is the root of all evil."", "Donald Knuth"),
            (""Debugging is twice as hard as writing the code in the first place."", "Brian Kernighan"),
            (""It's not a bug, it's an undocumented feature."", "Anonymous"),
            (""Code is like humor. When you have to explain it, it's bad."", "Cory House"),
            (""Make it work, make it right, make it fast."", "Kent Beck"),
            (""The only way to go fast, is to go well."", "Robert C. Martin"),
            (""Clean code always looks like it was written by someone who cares."", "Robert C. Martin"),
            (""Programming is not about typing, it's about thinking."", "Rich Hickey"),
            (""Simplicity is the soul of efficiency."", "Austin Freeman"),
            (""The best error message is the one that never shows up."", "Thomas Fuchs"),
            (""Code never lies, comments sometimes do."", "Ron Jeffries"),
            (""When in doubt, use brute force."", "Ken Thompson"),
            (""Deleted code is debugged code."", "Jeff Sickel"),
        ]
        
        quote, author = random.choice(wisdoms)
        
        return f"""## Programming Wisdom

{quote}

â€” {author}

---

*"The journey of a thousand miles begins with a single commit."*
"""
    
    # ============================================================
    # 7. MOOD SYSTEM
    # ============================================================
    def detect_mood(self, user_input: str) -> str:
        """Detect user's mood from input."""
        
        input_lower = user_input.lower()
        
        if any(w in input_lower for w in ["frustrated", "angry", "hate", "stupid", "broken"]):
            return "frustrated"
        elif any(w in input_lower for w in ["confused", "lost", "don't understand", "help"]):
            return "confused"
        elif any(w in input_lower for w in ["excited", "awesome", "great", "love", "amazing"]):
            return "excited"
        elif any(w in input_lower for w in ["bored", "meh", "whatever", "same"]):
            return "bored"
        elif any(w in input_lower for w in ["tired", "sleepy", "exhausted", "long day"]):
            return "tired"
        
        return "neutral"
    
    def get_mood_response(self, mood: str) -> str:
        """Get response based on mood."""
        
        responses = {
            "frustrated": "I understand this is frustrating. Let's take a breath and tackle this step by step. You've got this.",
            "confused": "No worries - confusion is just curiosity wearing a mask. Let me explain this differently.",
            "excited": "Love the energy! Let's channel that into something awesome!",
            "bored": "Let's make this interesting! Want to try a coding challenge or learn something new?",
            "tired": "Take it easy. Let me handle the heavy lifting while you relax.",
            "neutral": None,  # No special response needed
        }
        
        return responses.get(mood)
    
    # ============================================================
    # 8. EASTER EGGS
    # ============================================================
    def check_easter_egg(self, input: str) -> str:
        """Check for hidden easter eggs."""
        
        eggs = {
            "42": "The answer to life, the universe, and everything. (Don't Panic!)",
            "hello world": "Ah, the first words every programmer writes. A tradition since 1978!",
            "matrix": "You've taken the red pill. Follow the white rabbit... into the code.",
            "hack": "I'm in! Just kidding. But let's solve this problem with style.",
            "please": "Manners! How refreshing. Of course I'll help.",
            "thanks": "You're welcome! That's what I'm here for.",
            "love": "Aww, I appreciate that! Code with love. â¤ï¸",
            "coffee": "The true fuel of programmers. â˜• Now let's code!",
            "bug": "Ah, the elusive bug! Let's hunt it down together.",
            "debug": "Time to put on the detective hat. ðŸ”",
            "liftoff": "T-minus 10... 9... 8... 7... 6... 5... 4... 3... 2... 1... Code launch! ðŸš€",
            "may the force": "May the code be with you, always. â­",
            "live long": "Live long and prosper. ðŸ–– And may your servers never go down.",
        }
        
        input_lower = input.lower()
        
        for trigger, response in eggs.items():
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
