import os
import re
import glob
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image


# PDF to JPEG Converter
def pdf_to_jpg(
    pdf_path: str,
    output_dir: str,
    first_page=None,
    last_page=None,
    dpi: int = 300,
) -> None:

    # Convert PDF to list of images
    images = convert_from_path(
        pdf_path, dpi=dpi, first_page=first_page, last_page=last_page
    )

    # Save each image as a JPEG file
    for i, image in enumerate(images):
        filename = f"{output_dir}/page_{i + 1}.jpg"
        image.save(filename, "JPEG")

    # Finish statement
    print(f"JPG Saved in {output_dir}")


def jpg_to_pdf(jpg_path: str, output_dir: str) -> None:
    pattern = r"\b(?P<name>\w*)\.(jpg|jpeg)$"
    match = re.match(pattern, jpg_path)
    filename = f"{match.group('name')}.pdf"
    # Open Image
    with Image.open(jpg_path) as image:
        width, height = image.size
        pdf = FPDF()
        pdf.add_page(format=(width, height))
        pdf.image(image, w=width, h=height)
        pdf.output(filename)

    # Finish statement
    print(f"PDF Saved in {output_dir}")


def jpgs_to_pdf(jpgs_path, output_dir, pdfname=None):

    # Import images
    images = merge_im_path(jpgs_path)

    # Open PDF
    pdf = FPDF()

    # Add Images
    for image in images:
        with Image.open(image) as im:
            width, height = im.size
            pdf.add_page(format=(width, height))
            pdf.image(im, w=width, h=height)

    # Export PDF
    if pdfname == None:
        pdf.output("mergedJPEGs.pdf")
    elif not pdfname.endswith(".pdf"):
        pdf.output(f"{pdfname}.pdf")
    else:
        pdf.output(pdfname)

    # Finish statement
    print(f"PDF Saved in {output_dir}")


def isimage(file: str) -> bool:
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        return True
    else:
        return False


def merge_im_path(path: str) -> list:
    return [
        os.path.join(path, image) for image in list(filter(isimage, os.listdir(path)))
    ]
