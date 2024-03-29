#!/usr/bin/env python

"""
A chat service that uses the OpenAI API to generate responses.
"""

import argparse
import json
import os
import readline  # pylint: disable=unused-import
from datetime import datetime
from os import path
from sys import stdout
from typing import NamedTuple, Optional

from openai import OpenAI

client = OpenAI()


class ChatCompletionParams(NamedTuple):
    """
    Parameters for the chat completion API.

    See API docs for details
    https://platform.openai.com/docs/api-reference/chat
    """

    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = None
    n: int = 1
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: dict = {}
    user: str = ""


class ChatConfig(NamedTuple):
    """
    Configuration for the chat service.
    """

    context: str = ""
    params: ChatCompletionParams = ChatCompletionParams()


class ChatService:
    """
    A chat service that uses the OpenAI API to generate responses.

    Attributes
    ----------
    context : str
        The context for the conversation.
    history : ChatHistory
        The conversation history.
    params : ChatCompletionParams
        The parameters for the chat completion API.
    """

    def __init__(
        self,
        config=ChatConfig(),
    ):
        """
        Parameters
        ----------
        config : ChatConfig
            The configuration for the chat service.
        """
        self.context = config.context
        self.params = config.params

        self.history = ChatHistory(context=config.context)

    def start(self) -> None:
        """Start the chat service."""
        print('Type "/help" to see available commands.\n')

        try:
            while True:
                line = input(">>> ")
                if line == "":
                    continue
                if line == "/help":
                    self.handle_command_help()
                    continue
                if line == "/log":
                    self.handle_command_log()
                    continue
                if line == "/save":
                    self.handle_command_save()
                    continue
                if line == "/clear":
                    self.handle_command_clear()
                    continue
                if line == "/forget":
                    self.handle_command_forget()
                    continue
                if line == "/context":
                    self.handle_command_context()
                    continue
                if line == "/exit":
                    break

                self.stream_completion(line, self.params)

        except (KeyboardInterrupt, EOFError):
            pass
        except Exception as e:
            print(e)
            raise
        finally:
            print("\nGoodbye!\n")

    def handle_command_help(self) -> None:
        """Print the help message."""
        print(
            """
/help    - view available commands
/exit    - exit the program
/log     - view the current conversation log
/save    - save the conversation log to a file
/clear   - clear all the conversation log
/forget  - cancel the previous message
/context - show the current chat context
"""
        )

    def handle_command_log(self) -> None:
        """Print the conversation log."""
        log = self.history.get_log()
        if log:
            print(f"\n\033[96m{log}\033[00m\n")
        else:
            print("\nempty\n")

    def handle_command_save(self) -> None:
        """Save the conversation log to a file."""
        file_path = self.history.save_log()
        print("\nsaved: " + file_path + "\n")

    def handle_command_clear(self) -> None:
        """Clear all the history of the conversation."""
        self.history.clear_log()
        print("\ncleared\n")

    def handle_command_forget(self) -> None:
        """Delete the last message in the conversation."""
        self.history.remove_last_conversation()
        previous_message = self.history.get_last_message()
        if previous_message is not None:
            print("\n" + previous_message["content"] + "\n")

    def handle_command_context(self) -> None:
        """Show the current context."""
        print("\n" + self.context + "\n")

    def create_prompt_messages(self, line: str) -> list:
        """Create a prompt for the AI to complete."""
        messages = []
        context = self.context.strip()
        if context:
            messages.append({"role": "system", "content": context})
        log = self.history.get_messages()
        if log:
            messages.extend(log)
        prompt = {"role": "user", "content": line}
        messages.append(prompt)
        self.history.add_message(prompt)
        return messages

    def stream_completion(self, line: str, params: ChatCompletionParams) -> None:
        """Stream completions to stdout as they become available."""
        messages = self.create_prompt_messages(line)

        stream = client.chat.completions.create(
            stream=True,
            messages=messages,
            **params._asdict(),
        )

        stdout.write("\n")
        buf = ""
        for obj in stream:
            choice = obj.choices[0]
            delta = choice.delta
            if delta.content:
                content = delta.content
                # don't print initial empty lines
                if buf != "" or not content.strip() == "":
                    stdout.write(content)
                    stdout.flush()
                    buf += content
        buf = buf.strip()
        stdout.write("\n\n")
        self.history.add_message({"role": "assistant", "content": buf})


class ChatHistory:
    """
    The history of the conversation.

    Attributes
    ----------
    context : str
        The context for the conversation.
    messages : list[dict]
        The messages in the conversation.
    """

    def __init__(self, context=""):
        self.context = context
        self.messages = []

    def add_message(self, message: dict) -> None:
        """Add a new message to the conversation."""
        self.messages.append(message)

    def get_messages(self) -> list:
        """Return the messages in the conversation."""
        return self.messages

    def get_last_message(self) -> Optional[dict]:
        """Return the last message in the conversation."""
        return self.messages[-1] if self.messages else None

    def remove_last_conversation(self) -> None:
        """Remove the last message in the conversation."""
        if self.messages:
            self.messages = self.messages[:-2]

    def get_log(self) -> str:
        """Return the text of the conversation log."""
        log = ""
        for message in self.messages:
            if message["role"] == "user":
                log += ">>> " + message["content"].strip() + "\n\n"
            if message["role"] == "assistant":
                log += message["content"].strip() + "\n\n"
        log = log.strip()
        return log

    def save_log(self) -> str:
        """Save the conversation log to a file and return the path."""
        home_dir = path.expanduser("~")
        log_dir = path.join(home_dir, ".ai", "log")
        if not path.exists(log_dir):
            os.makedirs(log_dir)
        now = datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%S") + ".jsonl"
        file_path = path.join(log_dir, file_name)

        with open(file_path, mode="w", encoding="utf-8") as f:
            context = {"role": "system", "content": self.context}
            log = json.dumps(context, ensure_ascii=False) + "\n"
            log += "\n".join([json.dumps(m, ensure_ascii=False) for m in self.messages])
            f.write(log)
        return file_path

    def clear_log(self) -> None:
        """Clear the conversation log."""
        self.messages.clear()


def read_args() -> argparse.Namespace:
    """Create a CompletionParams object from command line arguments."""
    default = ChatCompletionParams()

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", default=default.model)
    parser.add_argument("-M", "--max_tokens", type=int, default=default.max_tokens)
    parser.add_argument("-t", "--temperature", type=float, default=default.temperature)

    return parser.parse_args()


def create_chat_config() -> ChatConfig:
    """Create a ChatConfig object from command line arguments."""
    context = load_context()

    args = read_args()
    params = ChatCompletionParams(**vars(args))

    config = ChatConfig(context=context, params=params)
    return config


def load_context() -> str:
    """Read the chat context from `~/.ai/context.txt` and return as a string."""
    home_dir = path.expanduser("~")
    context_file = path.join(home_dir, ".ai", "context.txt")

    context = ""

    now = datetime.now()
    current_time = now.strftime("%a, %b %d %Y %I:%M %p")
    timezone = now.astimezone().tzname()
    context += f"Current time: {current_time} {timezone}\n\n"

    if path.exists(context_file):
        with open(context_file, mode="r", encoding="utf-8") as f:
            context += f.read().strip()
    return context


def main():
    """Start the chat service."""
    config = create_chat_config()
    chat = ChatService(config=config)
    chat.start()


if __name__ == "__main__":
    main()
