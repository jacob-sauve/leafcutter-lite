# leafcutter lite 🍁🐜......


-------------
_Note: this project has the same root as [leafcutter](https://github.com/jacob-sauve/leafcutter/tree/main), except does not involve the participation of Claude Code, which seemingly brought the old repository to a near-unsalvageable state of disrepair._

-------------

>_"Yet you, my creator, detest and spurn me, thy creature, to whom thou art bound by ties only dissoluble by the annihilation of one of us."_ -Mary Shelley, _Frankenstein_

<br>

What if you could have Claude CLI without Internet access or API tokens?

This is the question that **leafcutter** aims to answer: like the eponymous ants, our software aims to multiply the power of tiny, local models to pick up this heavy mantle, except now for free and open source! Claude has officially helped build its own successor.

## Concept
<img width="858" height="531" alt="leafcutter" src="https://github.com/user-attachments/assets/36758272-bfb8-4801-8015-83cae842d12c" />

1. The user starts by sending a message to the LLM, which the system injects into a premade prompt to encourage said LLM to perform tool calls when relevant.
2. The LLM produces grammar-constrained JSON output, potentially containing tool call information if relevant.
3. The JSON is parsed by the system, which then runs tool calls if present.
4. The system displays output to the user, summarising performed tool calls and showing any message provided by the LLM.

## Installation

Install ollama, e.g. on Brew
```
brew install ollama
```
Clone this repo
```
git clone github.com/jacob-sauve/leafcutter-lite
```
Make a venv
```
python3 -m venv .venv/
```
Install the dependencies
```
pip3 install -r requirements.txt
```
And run it!
```
python3 main.py
```

## Functionality
⚠️**CURRENTLY NO SAFEGUARDS TO FUNCTION CALLING; USER BEWARE**⚠️
<br>
<br>
leafcutter agents can currently:
- list files in a directory
- write to files in a directory
- append to files in a directory
- or chat normally!
Just ask the agent to do something, it should probably happen!
