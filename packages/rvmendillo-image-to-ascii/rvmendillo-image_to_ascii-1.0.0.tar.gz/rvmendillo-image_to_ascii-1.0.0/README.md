# ImageToASCII

It generates and saves ASCII texts and colored images from pixels of a JPEG file.

## Installation

Use the package manager [pip][pip-url] to install rvmendillo-image_to_ascii.

```bash
pip install rvmendillo-image_to_ascii
```

## Usage

```python
# Imports the ImageToASCII class from the rvmendillo-image_to_ascii package
from rvmendillo-image_to_ascii import ImageToASCII

# Instantiates the converter with a JPEG file
app = ImageToASCII('test_image.jpg')

# Generates ASCII text with a target width of 300 pixels
ascii_text = app.generate_ascii_text(300)

# Generates inverted ASCII text for black background
inverted_ascii_text = app.generate_ascii_text(300, inverted=True)

# Generates colored ASCII image for white background
colored_ascii_image = app.generate_colored_ascii_image(300, inverted=False)

# Generates inverted, colored ASCII image for black background
inverted_colored_ascii_image = app.generate_colored_ascii_image(300)

# Saves ASCII text in a TXT file
app.save_text(ascii_text, 'ascii_text.txt')

# Saves inverted ASCII text in a TXT file
app.save_text(inverted_ascii_text, 'inverted_ascii_text.txt')

# Saves colored ASCII image
app.save_image(colored_ascii_image, 'colored_ascii_image.png')

# Saves inverted, colored ASCII image
app.save_image(inverted_colored_ascii_image, 'inverted_colored_ascii_image.png')
```

## License
[MIT][mit-license]

[pip-url]: https://pip.pypa.io/en/stable/
[mit-license]: https://choosealicense.com/licenses/mit/