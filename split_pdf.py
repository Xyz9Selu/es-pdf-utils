#!/usr/bin/env python3
import fitz  # PyMuPDF
import argparse
from pathlib import Path

def parse_split_ratio(ratio_str):
    """
    Parse split ratio string like 'h35:36:37' into a list of ratios
    Returns: list of ratios that sum up to 1.0
    """
    if not ratio_str.startswith('h'):
        return [1.0]  # no split
    
    # Extract numbers after 'h'
    numbers = [int(x) for x in ratio_str[1:].split(':')]
    total = sum(numbers)
    return [n/total for n in numbers]

def split_pdf_page(input_pdf, output_pdf, split_config):
    """
    Split PDF pages according to ratio configuration.
    split_config format: 'h1:1,1,h35:36:37' means:
    - first page splits horizontally with ratio 1:1
    - second page no split
    - third page and remaining pages split horizontally with ratio 35:36:37
    """
    # Parse split configuration
    splits = []
    for part in split_config.split(','):
        splits.append(parse_split_ratio(part))

    # Open the input PDF
    doc = fitz.open(input_pdf)
    # Create a new PDF for output
    out_doc = fitz.open()
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Get split ratios for current page
        ratios = splits[min(page_num, len(splits) - 1)]
        
        if len(ratios) == 1:
            # No split needed, just copy the page
            out_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        else:
            # Calculate dimensions
            page_width = page.rect.width
            page_height = page.rect.height
            
            # Keep track of current position
            current_x = 0
            
            # Create splits
            for ratio in ratios:
                split_width = page_width * ratio
                
                # Create a new page with appropriate size
                new_page = out_doc.new_page(width=split_width, height=page_height)
                
                # Calculate the source rectangle for this section
                src_rect = fitz.Rect(
                    current_x,        # left
                    0,                # top
                    current_x + split_width,  # right
                    page_height       # bottom
                )
                
                # Calculate the destination rectangle
                dest_rect = fitz.Rect(
                    0,              # left
                    0,              # top
                    split_width,    # right
                    page_height     # bottom
                )
                
                # Copy the section of the original page
                new_page.show_pdf_page(dest_rect, doc, page_num, clip=src_rect)
                
                # Update current position
                current_x += split_width
    
    # Save the output PDF
    out_doc.save(output_pdf)
    out_doc.close()
    doc.close()

def main():
    parser = argparse.ArgumentParser(description='Split PDF pages horizontally with specified ratios')
    parser.add_argument('input_pdf', help='Input PDF file path')
    parser.add_argument('output_pdf', help='Output PDF file path')
    parser.add_argument('split_config', 
                      help='Split configuration (e.g., "h1:1,1,h35:36:37" for first page 1:1, '
                           'second page no split, third page and remaining pages 35:36:37)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input_pdf).exists():
        print(f"Error: Input file '{args.input_pdf}' does not exist")
        return
    
    try:
        split_pdf_page(args.input_pdf, args.output_pdf, args.split_config)
        print(f"Successfully split PDF. Output saved to: {args.output_pdf}")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()
