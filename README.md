# PDF Utils

A collection of Python utilities for PDF manipulation. Currently includes functionality for splitting PDF pages horizontally with custom ratios.

## Features

- Split PDF pages horizontally with customizable ratios
- Support for different split configurations per page
- Maintains original page quality and content

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pdf-utils.git
cd pdf-utils
```

2. Install the required dependencies:
```bash
pip install PyMuPDF
```

## Usage

### Split PDF Pages

The `split_pdf.py` script allows you to split PDF pages horizontally with specified ratios.

```bash
python split_pdf.py input.pdf output.pdf "split_config"
```

#### Parameters:
- `input.pdf`: Path to the input PDF file
- `output.pdf`: Path where the output PDF will be saved
- `split_config`: Configuration string specifying how to split pages

#### Split Configuration Format:
The split configuration is a comma-separated string where each part represents the split ratio for a page:
- `h1:1` means split the page horizontally into two equal parts
- `1` (or any number without 'h') means no split for that page
- The last configuration is used for all remaining pages

#### Examples:

1. Split all pages equally in half:
```bash
python split_pdf.py input.pdf output.pdf "h1:1"
```

2. Split first page in half, keep second page whole, split remaining pages in ratio 35:36:37:
```bash
python split_pdf.py input.pdf output.pdf "h1:1,1,h35:36:37"
```

## Requirements

- Python 3.6 or higher
- PyMuPDF (fitz)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
