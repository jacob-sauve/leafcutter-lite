"""
leafcutter
making small llms pull their weight
RIP Claude CLI
"""
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import os
from os.path import exists, isfile
import json


MODEL = "gemma3:270m"

SYSTEM_PROMPT = '''You are a desktop assistant. You can call tools by responding with JSON.

Available tools:
- list_files: {{"tool": "list_files", "args": {{"directory": "<path>"}}}}
- write_to_file: {{"tool": "write_to_file", "args": {{"filepath": "<path>", "contents": "<text>", "append", "<bool>"}}}}
- append_to_file: {{"tool": "write_to_file", "args": {{"filepath": "<path>", "contents": "<text>"}}}}

Example:
User: add the line 'foxes' to recipes.txt
Response: {{"tool": "append_to_file", "args": {{"filepath": "recipes.txt", "contents": "foxes"}}}} 

If the user wants you to use a tool, respond ONLY with the JSON object. ALWAYS include NONEMPTY args!
If no tool is needed, respond with: {{"tool": null, "message": "<your reply>"}}
'''


def write_file(filepath, contents, append=False):
    if not (exists(filepath) and not isfile(filepath)):
        mode = "a" if append else "w"
        with open(filepath, mode) as file:
            file.write(contents)
        return f"wrote {filepath}"
    return f"error: {filepath} is a directory"

@tool
def list_files(directory="."):
    """Get list of files in specified directory, default in working directory."""
    return [f for f in os.listdir(directory) if isfile(os.path.join(directory, f))]


@tool
def write_to_file(filepath, contents, append=False):
    """
    Write contents to file at filepath.
    Default overwrites file if append unspecified or False, adds to file instead if append is True.
    """
    return write_file(filepath, contents, append)

@tool
def append_to_file(filepath, contents):
    """Append contents to file at filepath."""
    return write_file(filepath, "\n"+contents, append=True)


TOOL_MAP = {t.name: t for t in [list_files, write_to_file, append_to_file]}


if __name__ == "__main__":

    agent = ChatOllama(model=MODEL, format="json")
    prompt = ChatPromptTemplate.from_messages([
        ('system', SYSTEM_PROMPT + '\n\nERROR: {error}'),
        ('user', '{question}')
        ])
    chain = prompt | agent

    while True:
        user_msg = input("> ")

        response = chain.invoke({'question': user_msg, 'error': 'None, all good.'})

        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            print("AI: ", response.content)
            continue

        tool_name = data.get("tool")

        if tool_name and tool_name in TOOL_MAP:
            args = data.get("args", {})
            try:
                print(f"[calling {tool_name} with {args}]")
                result = TOOL_MAP[tool_name].invoke(args)
                print(f"[result: {result}]")
            except:
                while not args:
                    response = chain.invoke({'question': user_msg, 'error': 'args required for function call. Please try function call again with ALL valid arguments specified.'})
                    print("Loading...")
                    data = json.loads(response.content)
                    args = data.get("args", {})
                print(f"[calling {tool_name} with {args}]")
                result = TOOL_MAP[tool_name].invoke(args)
                print(f"[result: {result}]")
        elif tool_name is None:
            print("AI: ", data.get("message", response.content))
        else:
            print(f"[unknown tool: {tool_name}]")
            print("AI: ", response.content)
