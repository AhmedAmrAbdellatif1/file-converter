import os
import sys
import re
import PyPDF2
from pdf2image import convert_from_path
from tqdm import tqdm
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
    # Count pages before conversion
    with open(pdf_file, "rb") as pdf:
        pdf_reader = PyPDF2.PdfReader(pdf)
        num_pages = len(pdf_reader.pages)

    # Convert PDF to a list of images (one image per page)
    try:
        if num_pages > 100:
            print("\nℹ️  the PDF file exceeds 100 pages")
            images = convert_from_path(
                pdf_file,
                dpi=dpi,
                first_page=first_page,
                last_page=last_page,
                fmt="jpg",
                output_folder=output_dir,
            )
        else:
            images = convert_from_path(
                pdf_file,
                dpi=dpi,
                first_page=first_page,
                last_page=last_page,
            )
            # Save each page image as a JPEG file
            with tqdm(total=num_pages, desc="Processing", unit="step") as pbar:
                for i, image in enumerate(images):
                    filename = f"{output_dir}/page_{i + 1}.jpg"
                    image.save(filename, "JPEG")
                    pbar.update(1)  # Update the progress bar by 1 step

    except:
        sys.exit(
            f"\n⚠️  Couldn't open file {pdf_file}: Change the arabic name in the parsed path"
        )

    # Print completion message
    if images == []:
        print(f"\n⚠️  No output; Empty PDF imported")
    elif not last_page == None and last_page > num_pages:
        print(
            "\nℹ️  Last page number parsed is greater than the PDF; Conversion is limited by the PDF size"
        )
    else:
        print(f"\n✅  JPGs Saved in {output_dir}")


# JPEG to PDF Converter (for a list of images)
def jpg_to_pdf(images: list, output_dir: str) -> None:
    """
    Converts a list of JPEG images into a single PDF file.

    Parameters:
    - images: List of paths to JPEG images to be converted.
    - output_dir: Directory where the output PDF will be saved.
    """

    # Extract the base name for the output PDF from the first image filename
    pattern = r"\b(?P<name>[\w\-\s\(\)]+)\.(jpg|jpeg)$"
    match = re.search(pattern, images[0])
    if match:
        filename = f"converted-{match.group('name')}.pdf"
    else:
        filename = "converted.pdf"

    pdf = FPDF()

    # Add each JPEG as a new page in the PDF
    total_steps = len(images)  # Define the total steps for the loading bar
    with tqdm(total=total_steps, desc="Processing", unit="step") as pbar:
        for image in images:
            with Image.open(image) as im:
                width, height = im.size
                pdf.add_page(format=(width, height))
                pdf.image(im, w=width, h=height)
            pbar.update(1)  # Update the progress bar by 1 step

    # Save the PDF file
    pdf.output(os.path.join(output_dir, filename))

    # Print completion message
    print(f"\n✅  PDF Saved in {output_dir}")


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
    total_steps = len(pdfs)  # Define the total steps for the loading bar
    with tqdm(total=total_steps, desc="Processing", unit="step") as pbar:
        for pdf in pdfs:
            merger.append(pdf)
            pbar.update(1)  # Update the progress bar by 1 step

    # Write the merged PDF to the output directory
    output_path = os.path.join(output_dir, "merged-pdfs.pdf")
    merger.write(output_path)

    # Print completion message
    print(f"\n✅  PDF Saved in {output_path}")


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
    total_steps = len(reader.pages)  # Define the total steps for the loading bar
    with tqdm(total=total_steps, desc="Processing", unit="step") as pbar:
        for page in reader.pages:
            page.compress_content_streams()  # Compress the content streams of the page
            writer.add_page(page)  # Add the compressed page to the writer
            pbar.update(1)  # Update the progress bar by 1 step

    # Save the compressed PDF to the specified output directory
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        writer.write(f)

    # Print completion message
    print(f"\n✅  Compressed PDF saved in {output_dir}")
