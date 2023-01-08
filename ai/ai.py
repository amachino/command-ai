#!/usr/bin/env python

import argparse
import datetime
import os
import readline
import sys
from os import path

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# See API docs
# https://beta.openai.com/docs/api-reference/completions

DEFAULT_OPTIONS = {
    "model": "text-davinci-003",
    "prompt": "",
    "suffix": None,
    "max_tokens": 1000,
    "temperature": 0.5,
    "top_p": None,
    "n": 1,
    "stream": True,
    "logprobs": None,
    "echo": False,
    "stop": ">>> ",
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "best_of": 1,
    "logit_bias": {},
    "user": "",
}

log = ""


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model")
    parser.add_argument("-M", "--max_tokens", type=int)
    parser.add_argument("-t", "--temperature", type=float)

    args = parser.parse_args()
    return args


def request_completion(**kwargs):
    option = DEFAULT_OPTIONS.copy()

    for k, v in kwargs.items():
        if v is not None:
            option[k] = v

    response = openai.Completion.create(**option)
    return response


def print_completion_stream(**kwargs):
    option = kwargs.copy()
    option["stream"] = True
    option["n"] = 1

    stream = request_completion(**option)

    sys.stdout.write("\n")
    buf = ""
    for obj in stream:
        text = obj.choices[0].text
        if buf != "" or text != "\n":
            sys.stdout.write(text)
            sys.stdout.flush()
            buf += text

    global log
    log += buf.strip() + "\n\n\n"


def create_prompt(line):
    global log
    log += f">>> {line}\n\n"

    propmt = log[-3000:]
    return propmt


def print_log():
    print(f"\n\033[96m{log.strip()}\033[00m\n\n")


def save_log():
    home_dir = path.expanduser("~")
    log_dir = path.join(home_dir, ".ai", "log")
    if not path.exists(log_dir):
        os.makedirs(log_dir)
    now = datetime.datetime.now()
    file_name = now.strftime("%Y%m%d%H%M%S") + ".txt"
    file_path = path.join(log_dir, file_name)
    with open(file_path, mode="w") as f:
        f.write(log)
    print(f"saved: {file_path}")


def clear_log():
    global log
    log = ""
    print("cleared")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable.")
        exit()

    args = parse_args()
    try:
        while True:
            line = input(">>> ")
            if line == "exit":
                break
            if line == "log":
                print_log()
                continue
            if line == "save":
                save_log()
                continue
            if line == "clear":
                clear_log()
                continue
            prompt = create_prompt(line)
            print_completion_stream(
                prompt=prompt,
                model=args.model,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            print("\n\n")
    except (KeyboardInterrupt, EOFError):
        pass
    except openai.error.InvalidRequestError as e:
        print(e)
    finally:
        print("\nGoodbye!\n\n")
        exit()


if __name__ == "__main__":
    main()
