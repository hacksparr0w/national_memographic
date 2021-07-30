from . import meme


def main():
    template = meme.load_template("drakeposting")
    captions = (
        "Making a meme in an image editor",
        "Generating a meme using a Twitter bot"
    )

    image = meme.render(template, captions)
    image.transform(resize="x600")
    image.save(filename="intro.png")


if __name__ == "__main__":
    main()
