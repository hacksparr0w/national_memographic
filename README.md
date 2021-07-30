![Introduction][1]

## Usage

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

## Roadmap
 - [ ] Implement a general-purpose meme generation library.
 - [ ] Build a simple Twitter bot that lets Twitter users make memes easily.
 - [x] Profit!

[1]: https://raw.githubusercontent.com/hacksparr0w/national_memographic/main/intro.png
