<h1 align="center">
  <br>
    <img
        src="https://raw.githubusercontent.com/hacksparr0w/national_memographic/main/mascot.png"
        alt="National Memographic"
        width="580"
    >
  <br>
    National Memographic
  <br>
</h1>

<h4 align="center">The one and only Twitter meme bot</h4>

National Memographic is a very simple Twitter bot allowing you to create memes directly from Twitter DMs - you simply send a message with parameters specifying what meme template you want to use and what text to caption the template with and this artificially intelligent bot will take care of the rest, creating you a crispy meme according to your desires.

If you are a little bit more technically proficient user, you can try using National Memographic's programmatic Python interface or interact with it via terminal.

__Main features__:
 - [x] General-purpose meme generation Python package allowing you to make watermark-free memes fast and simple,
 - [x] User-friendly interfaces accessible through Python code, terminal and even Twitter DMs,
 - [ ] Rich meme template library,
 - [ ] Advanced features like GIF captioning and media embedding,
 - [ ] Integration with Twitter's webhooks for real-time direct message processing.

## Installation

National Memographic can be installed using [pip][1]:

```bash
pip install national_memographic
```

## Usage

### Python

You can use the core library as a tool for programmatic meme generation. The
following is a simple API demonstration.

```python
from national_memographic import meme


template = meme.load_template("drakeposting")
captions = (
    "Making a meme in an image editor",
    "Generating a meme using a Twitter bot"
)

image = meme.caption(template, captions)
image.transform(resize="x600")
image.save(filename="intro.png")
```

To see all available meme templates, simply execute the
`meme.load_templates()` function and try browsing through the output list.

### CLI

National Memographic also comes with a simple command-line interface. Here is
a command for achieving the exact same results as the programmatic example,
from the comfort of your shell.

```bash
meme caption --out intro.png drakeposting "Making a..." "Generating a..."
```

You can also list all available meme templates by running `meme ls`, or view
help for the whole CLI app by typing `meme --help`.

## Contributing

If you'd like us to add your favorite meme template or have an idea for a new
feature, you are highly encouraged to contact us or open a new issue.

[1]: https://pypi.org/project/pip/
