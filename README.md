![Introduction][1]

## Installation

You can currently install National Memographic by using the
[Poetry dependency manager][2]. Following are the recommended steps to take
when installing with Poetry.

```bash
git clone https://github.com/hacksparr0w/national_memographic
cd national_memographic

poetry build
pip install dist/national_memographic-0.1.0.tar.gz
```

_Note: The actual version of the built package may vary._

## Usage

### Library

You can use the core library as a tool for programmatic meme generation. The
following is a simple API demonstration.

```python
from national_memographic import meme


template = meme.load_template("drakeposting")
captions = (
    "Making a meme in an image editor",
    "Generating a meme using a Twitter bot"
)

image = meme.render(template, captions)
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
meme generate --out intro.png drakeposting "Making a..." "Generating a..."
```

You can also list all available meme templates by running `meme ls`, or view
help for the whole CLI app by typing `meme --help`.

## Roadmap
 - [ ] Implement a general-purpose meme generation library.
 - [ ] Build a simple Twitter bot that lets Twitter users make memes easily.
 - [x] Profit!

[1]: https://raw.githubusercontent.com/hacksparr0w/national_memographic/main/intro.png
[2]: https://github.com/python-poetry/poetry
