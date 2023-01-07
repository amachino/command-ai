# command `ai`

This is a command-line interface (CLI) that allows you to interact with the OpenAI API to generate text completions. You can use it to generate natural language responses to prompts, or to complete a given text.


## Requirements

- Python 3
- OpenAI API key - obtain one from [here](https://beta.openai.com/signup/).


## Installation

1. Clone the repository and install by `pip install . ` inside the directory.
2. Set your OpenAI API key as an environment variable with the name `OPENAI_API_KEY`.
3. Run the CLI by using the command `ai`.


## Usage

Enter a prompt or some text you want to complete, and the AI will generate a response. You can also use the following commands:

- `exit` - exit the CLI.
- `log` - view the current conversation log.
- `save` - save the current conversation log to a file.
- `clear` - clear the current conversation log.

## Arguments

You can pass the following arguments to the CLI:

- `--model` - the model to use for generating text completions.
- `--max_tokens` - the maximum number of tokens (words) to generate in the completion.
- `--temperature` - a value that determines the creativity and unpredictability of the AI's responses. A higher temperature results in more random responses, while a lower temperature results in more deterministic responses.

See the [OpenAI API docs](https://beta.openai.com/docs/api-reference/completions) for details.


## Examples

```
% ai
```

```
>>> What is the meaning of life?

The meaning of life is subjective and can vary from person to person. For some, it may be to find purpose, joy, and fulfillment in life, while for others, it may be to make a difference in the world or to find inner peace.


>>> Translate it into Japanese

人生の意味は主観的で、人それぞれに異なります。一部の人にとっては、人生に目的、喜び、満足感を見つけることかもしれませんが、他の人にとっては、世界を変えることや内なる平和を見つけることかもしれません。


>>> For you?

For me, the meaning of life is to live a life of purpose, joy, and gratitude, and to make a positive impact on the world.
```
