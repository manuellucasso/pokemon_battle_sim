# pokemon\_battle\_sim

\# Python Pokémon Battle Simulator



A modular, terminal-based Pokémon battle engine built in Python. This project faithfully recreates official Pokémon battle mechanics, including complex damage calculations, status conditions, and multi-turn move effects, with a foundation designed to eventually support online multiplayer battles with friends and family.



\## 🏗️ Project Architecture



The simulator is built with a strong emphasis on modularity and clean state management, separating data parsing from battle logic:



\* \*\*`battle.py`\*\*: The core engine and turn router. It handles the battle loop, speed checks, and routes attacks to their specific effect functions.

\* \*\*`battle\_states.py`\*\*: A robust State Machine that manages pre-attack checks (e.g., Flinch, Recharge, Sleep) and end-of-turn effects (e.g., Leech Seed, Poison, Traps).

\* \*\*`battle\_effects.py`\*\*: The effect interpreter. It parses the `move\_set.csv` database to extract modifiers (accuracy drops, multi-hits, recoil) and passes flags back to the main engine.

\* \*\*`pokemon.py`\*\*: Contains the `Pokemon` class, managing base stats, dynamic battle multipliers (Accuracy/Evasion), and volatile status memory (Bide, Seeded, Trapped).

\* \*\*`data\_loader.py`\*\*: Handles loading and parsing the CSV move database.



\## ✨ Key Features



\* \*\*Accurate Damage Pipeline\*\*: Replicates official formulas including STAB (Same Type Attack Bonus), Type Effectiveness, and Critical Hits.

\* \*\*Conditional Effect Routing\*\*: Moves with secondary effects (like \*Bide\*, \*Leech Seed\*, or \*Explosion\*) are cleanly intercepted and processed without cluttering the main battle loop.

\* \*\*Dynamic Stat Modifiers\*\*: Real-time handling of in-battle stat stages, including specialized multipliers for Evasion and Accuracy.

\* \*\*Volatile Status Management\*\*: Tracks temporary battle conditions like Traps (\*Fire Spin\*, \*Bind\*) and Flinching.



\## 🚀 Getting Started



\### Prerequisites

\* Python 3.x

\* Standard libraries only (no external dependencies required yet).

