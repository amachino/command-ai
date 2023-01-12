# command `ai`

AI chatbot in your terminal, powered by OpenAI API.


## Requirements

- Python 3.7+
- OpenAI API key - obtain one from [here](https://beta.openai.com/signup/).


## Installation

1. Clone the repository and `cd` into it.
```
cd command-ai
```

2. Install the `ai` command by `pip install .`.
```
pip install .
```

3. Set your OpenAI API key as an environment variable.
```
export OPENAI_API_KEY="sk-..."
```


## Usage

Run the `ai` command in your terminal.

```
ai
```

Enter a prompt, and the AI will generate a response.

```
>>> Hello, who are you?↩
```

You can also use the following commands:

- `/help`   - view available commands
- `/exit`   - exit the program
- `/log`    - view the current conversation log
- `/save`   - save the conversation log to a file
- `/clear`  - clear all the conversation log
- `/forget` - cancel the previous message


## Arguments

You can pass the following arguments to the `ai` command:

- `-m, --model` - the model to use for generating text completions.
- `-M, --max_tokens` - the maximum number of tokens (words) to generate in the completion.
- `-t, --temperature` - a value that determines the creativity and unpredictability of the AI's responses. A higher temperature results in more random responses, while a lower temperature results in more deterministic responses.

See the [OpenAI API docs](https://beta.openai.com/docs/api-reference/completions) for details.


## Examples

```
% ai
Type "/help" to see available commands.

>>> What is the meaning of life?

The meaning of life is subjective and can vary from person to person. For some, it may be to find purpose, joy, and fulfillment in life, while for others, it may be to make a difference in the world or to find inner peace.


>>> Translate it into Japanese

人生の意味は主観的で、人それぞれに異なります。一部の人にとっては、人生に目的、喜び、満足感を見つけることかもしれませんが、他の人にとっては、世界を変えることや内なる平和を見つけることかもしれません。


>>> For you?

For me, the meaning of life is to live a life of purpose, joy, and gratitude, and to make a positive impact on the world.


>>> /exit

Goodbye!
```
