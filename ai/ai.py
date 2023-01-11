#!/usr/bin/env python

import argparse
import os
import readline
import sys
from datetime import datetime
from os import path
from sys import stdout
from typing import NamedTuple, Optional

import openai


class CompletionParams(NamedTuple):
    """
    Parameters for the completion API.

    See API docs for details
    https://beta.openai.com/docs/api-reference/completions
    """

    model: str = "text-davinci-003"
    prompt: str = None
    suffix: str = None
    max_tokens: int = 1000
    temperature: float = 0.5
    top_p: float = None
    n: int = 1
    stream: bool = True
    logprobs: int = None
    echo: bool = False
    stop: list[str] = [">>> "]
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    best_of: int = 1
    logit_bias: dict[str, int] = {}
    user: str = ""


class Message(NamedTuple):
    """A message in the conversation."""

    prompt: str
    completion: str


class ChatService:
    """
    A chat service that uses the OpenAI API to generate responses.

    Attributes
    ----------
    context : str
        The context for the conversation.
    history : ChatHistory
        The conversation history.
    memory : int
        The number of messages to remember.
    params : CompletionParams
        The parameters for the completion API.
    """

    def __init__(
        self,
        context="The following is a conversation with an AI program.",
        memory=3000,
        params=CompletionParams(),
    ):
        """
        Parameters
        ----------
        context : str
            The context for the conversation.
        memory : int
            The number of messages to remember.
        params : CompletionParams
            The parameters for the completion API.
        """
        self.context = context
        self.memory = memory
        self.params = params

        self.history = ChatHistory()

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
                if line == "/exit":
                    break

                self.stream_completion(line, self.params)

        except (KeyboardInterrupt, EOFError):
            pass
        except openai.error.InvalidRequestError as e:
            print(e)
        except Exception:
            raise
        finally:
            print("\nGoodbye!\n\n")

    def handle_command_help(self) -> None:
        """Print the help message."""
        print(
            """
/help   - view available commands
/exit   - exit the program
/log    - view the current conversation log
/save   - save the conversation log to a file
/clear  - clear all the conversation log
/forget - cancel the previous message

"""
        )

    def handle_command_log(self) -> None:
        """Print the conversation log."""
        log = self.history.get_log()
        stats = self.history.get_stats()
        if log:
            print(f"\n\033[92m{stats}\033[00m\n")
            print(f"\033[96m{log}\033[00m\n\n")
        else:
            print("empty")

    def handle_command_save(self) -> None:
        """Save the conversation log to a file."""
        file_path = self.history.save_log()
        print("saved: " + file_path)

    def handle_command_clear(self) -> None:
        """Clear all the history of the conversation."""
        self.history.clear_log()
        print("cleared")

    def handle_command_forget(self) -> None:
        """Delete the last message in the conversation."""
        self.history.remove_last_message()
        previous_message = self.history.get_last_message()
        if previous_message:
            print("\n" + previous_message.completion + "\n\n")

    def create_prompt(self, line: str) -> str:
        """Create a prompt for the AI to complete."""
        prompt = ""
        context = self.context.strip()
        if context:
            prompt += context + "\n\n\n"
        log = self.history.get_log()
        log = log[-self.memory :]
        if log:
            prompt += log + "\n\n\n"
        prompt += ">>> " + line + "\n"
        return prompt

    def stream_completion(self, line: str, params: CompletionParams) -> None:
        """Stream completions to stdout as they become available."""
        prompt = self.create_prompt(line)

        params = params._replace(prompt=prompt, stream=True, n=1)

        stream = openai.Completion.create(**params._asdict())

        stdout.write("\n")
        buf = ""
        for obj in stream:
            text = obj.choices[0].text
            if buf != "" or text != "\n":
                stdout.write(text)
                stdout.flush()
                buf += text
        buf = buf.strip()
        stdout.write("\n\n\n")
        message = Message(prompt=line, completion=buf)
        self.history.add_message(message)


class ChatHistory:
    """
    The history of the conversation.

    Attributes
    ----------
    messages : list[Message]
        The messages in the conversation.
    """

    def __init__(self):
        self.messages: list[Message] = []

    def add_message(self, message: Message) -> None:
        """Add a new message to the conversation."""
        self.messages.append(message)

    def remove_last_message(self) -> None:
        """Remove the last message in the conversation."""
        if self.messages:
            self.messages.pop()

    def get_last_message(self) -> Optional[Message]:
        """Return the last message in the conversation."""
        return self.messages[-1] if self.messages else None

    def get_stats(self) -> str:
        """Return the number of requests, characters, and bytes in the log."""
        n_reqs = len(self.messages)
        n_chars = len(self.get_log())
        n_bytes = len(self.get_log().encode("utf-8"))
        return f"{n_reqs} reqs / {n_chars} chars / {n_bytes} bytes"

    def get_log(self) -> str:
        """Return the text of the conversation log."""
        log = ""
        for message in self.messages:
            log += ">>> " + message.prompt.strip() + "\n\n"
            log += message.completion.strip() + "\n\n\n"
        log = log.strip()
        return log

    def save_log(self) -> str:
        """Save the conversation log to a file and return the path."""
        home_dir = path.expanduser("~")
        log_dir = path.join(home_dir, ".ai", "log")
        if not path.exists(log_dir):
            os.makedirs(log_dir)
        now = datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%S") + ".txt"
        file_path = path.join(log_dir, file_name)

        with open(file_path, mode="w") as f:
            stats = self.get_stats()
            log = self.get_log()
            f.write(stats + "\n\n" + log)
        return file_path

    def clear_log(self) -> None:
        """Clear the conversation log."""
        self.messages.clear()


def create_params_from_args() -> CompletionParams:
    """Create a CompletionParams object from command line arguments."""
    default = CompletionParams()

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", default=default.model)
    parser.add_argument("-M", "--max_tokens", type=int, default=default.max_tokens)
    parser.add_argument("-t", "--temperature", type=float, default=default.temperature)

    args = parser.parse_args()
    params = CompletionParams(**vars(args))
    return params


def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("Please set OPENAI_API_KEY environment variable.")
        exit()

    params = create_params_from_args()
    chat = ChatService(params=params)
    chat.start()


if __name__ == "__main__":
    main()
