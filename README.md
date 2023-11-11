# command `ai`

AI chatbot in your terminal, powered by OpenAI API.


## Requirements

- Python 3.8+
- OpenAI API key - obtain one from [here](https://platform.openai.com/api-keys).


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

- `/help`    - view available commands
- `/exit`    - exit the program
- `/log`     - view the current conversation log
- `/save`    - save the conversation log to a file
- `/clear`   - clear all the conversation log
- `/forget`  - cancel the previous message
- `/context` - show the current chat context

Optionally, you can create `~/.ai/context.txt` file to specify the chat context. The context will be used as the system prompt for the AI's responses.

An example of `~/.ai/context.txt` file:

```
The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
```

## Arguments

You can pass the following arguments to the `ai` command:

- `-m, --model` - ID of the model to use. Check available models [here](https://platform.openai.com/docs/models/models).
- `-M, --max_tokens` - The maximum number of tokens allowed for the generated answer. By default, the number of tokens the model can return will be (4096 - prompt tokens).
- `-t, --temperature` - What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

See the [OpenAI API docs](https://platform.openai.com/docs/api-reference/chat) for details.


## Examples

```
% ai
Type "/help" to see available commands.

>>> When will singularity happen?

It is difficult to predict exactly when the singularity will occur, as it depends on a variety of factors and is subject to ongoing debate and speculation among experts in the field of artificial intelligence. However, some estimates suggest that it could happen within the next few decades, as advances in technology continue to accelerate at an unprecedented rate. Ultimately, the timing and exact nature of the singularity will depend on a range of social, economic, and technological factors that are difficult to predict with certainty.

>>> Translate it into Japanese.

シンギュラリティがいつ起こるかを正確に予測することは難しいため、人工知能の専門家たちの間でも議論や予測が続いています。ただし、技術の進歩が前例のない速度で進んでいることを考慮すると、数十年以内に起こる可能性があるとされています。最終的にシンギュラリティの発生時期や正確な性質は、社会、経済、技術面などに関する幅広い要因に依存するため、確実に予測することは困難です。

>>> /exit

Goodbye!
```
