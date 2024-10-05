import os
import re
import glob
import PyPDF2
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image


# PDF to JPEG Converter
def pdf_to_jpg(
    pdf_file: str,
    output_dir: str,
    first_page=None,
    last_page=None,
    dpi: int = 300,
) -> None:
    """
    Converts a PDF file to a series of JPEG images.

    Parameters:
    - pdf_file: Path to the PDF file.
    - output_dir: Directory where the JPEG images will be saved.
    - first_page: (Optional) First page to convert.
    - last_page: (Optional) Last page to convert.
    - dpi: Resolution of the output JPEG images (default: 300 DPI).
    """

    # Convert PDF to a list of images (one image per page)
    images = convert_from_path(
        pdf_file, dpi=dpi, first_page=first_page, last_page=last_page
    )

    # Save each page image as a JPEG file
    for i, image in enumerate(images):
        filename = f"{output_dir}/page_{i + 1}.jpg"
        image.save(filename, "JPEG")

    # Print completion message
    print(f"JPG Saved in {output_dir}")


# JPEG to PDF Converter (for a list of images)
def jpg_to_pdf(images: list, output_dir: str) -> None:
    """
    Converts a list of JPEG images into a single PDF file.

    Parameters:
    - images: List of paths to JPEG images to be converted.
    - output_dir: Directory where the output PDF will be saved.
    """

    # Extract the base name for the output PDF from the first image filename
    pattern = r"\b(?P<name>\w*)\.(jpg|jpeg)$"
    match = re.match(pattern, images[0])
    filename = f"{match.group('name')}.pdf"

    pdf = FPDF()

    # Add each JPEG as a new page in the PDF
    for image in images:
        with Image.open(image) as im:
            width, height = im.size
            pdf.add_page(format=(width, height))
            pdf.image(im, w=width, h=height)

    # Save the PDF file
    pdf.output(os.path.join(output_dir, filename))

    # Print completion message
    print(f"PDF Saved in {output_dir}")
    
    
def merge_pdfs(pdfs: list, output_dir: str) -> None:
    """
    Merges multiple PDF files into a single PDF file.

    Parameters:
    - pdfs: List of paths to the PDF files to be merged.
    - output_dir: Directory where the merged PDF will be saved.
    """
    
    # Initialize PDF merger
    merger = PyPDF2.PdfMerger()

    # Append each PDF to the merger
    for pdf in pdfs:
        merger.append(pdf)

    # Write the merged PDF to the output directory
    output_path = os.path.join(output_dir, "merged-pdfs.pdf")
    merger.write(output_path)

    # Print completion message
    print(f"PDF Saved in {output_path}")
    

def compress_pdf(pdf: str, output_dir: str) -> None:
    """
    Compresses the content streams of a PDF file to reduce its size.
    
    Parameters:
    - pdf: Path to the PDF file to be compressed.
    - output_dir: Directory where the compressed PDF will be saved.
    """
    
    # Extract the base name for the compressed PDF output file
    pattern = r"\b(?P<name>\w*)\.(pdf)$"
    match = re.match(pattern, pdf)
    filename = f"compressed-{match.group('name')}.pdf"

    # Initialize the PDF reader and writer
    reader = PyPDF2.PdfReader(pdf)
    writer = PyPDF2.PdfWriter()

    # Compress each page's content streams and add it to the writer
    for page in reader.pages:
        page.compress_content_streams()  # Compress the content streams of the page
        writer.add_page(page)  # Add the compressed page to the writer

    # Save the compressed PDF to the specified output directory
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        writer.write(f)

    # Print completion message
    print(f"Compressed PDF saved in {output_dir}")

