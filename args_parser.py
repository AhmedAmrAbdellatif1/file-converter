import argparse
import os


# Configure Parsing options
def args_parser() -> dict:
    parser = argparse.ArgumentParser(description="File type conversion")

    # Adding subparsers
    subparsers = parser.add_subparsers(
        dest="converter", required=True, title="Available conversion types"
    )

    # Subparser for pdf2jpg
    parser_pdf2jpg = subparsers.add_parser("pdf2jpg", help="Convert PDF to JPEG")
    parser_pdf2jpg.add_argument(
        "-f",
        "--file",
        metavar="filename/path",
        help="PDF file to convert",
        type=str,
        required=True,
    )
    parser_pdf2jpg.add_argument(
        "-i",
        "--initial",
        metavar="page-number",
        help="Initial page number",
        type=int,
        default=None,
    )
    parser_pdf2jpg.add_argument(
        "-l",
        "--last",
        metavar="pagenumber",
        help="Last page number",
        type=int,
        default=None,
    )
    parser_pdf2jpg.add_argument(
        "-o",
        "--output",
        metavar="directory",
        help="Output directory",
        type=str,
        default=os.getcwd(),
    )

    # Subparser for jpg2pdf
    parser_jpg2pdf = subparsers.add_parser("jpg2pdf", help="Convert JPEG to PDF")
    parser_jpg2pdf.add_argument(
        "-f",
        "--file",
        metavar="filename/path",
        help="JPEG file to convert",
        type=str,
        required=True,
    )
    parser_jpg2pdf.add_argument(
        "-o",
        "--output",
        metavar="directory",
        help="Output directory",
        type=str,
        default=os.getcwd(),
    )
    
    # Subparser for jpgs2pdf
    parser_jpgs2pdf = subparsers.add_parser("jpgs2pdf", help="Merge JPEGs into PDF")
    parser_jpgs2pdf.add_argument(
        "-p",
        "--path",
        metavar="path",
        help="JPEGs path",
        type=str,
        required=True,
    )
    parser_jpgs2pdf.add_argument(
        "-n",
        "--name",
        metavar="pdfname",
        help="Merged PDF filename",
        type=str,
        default=None,
    )
    parser_jpgs2pdf.add_argument(
        "-o",
        "--output",
        metavar="directory",
        help="Output directory",
        type=str,
        default=os.getcwd(),
    )

    # Parse CLI
    args = parser.parse_args()

    # Create dict to collect args
    config = {}

    # Check if the convertible file exists
    if not os.path.isfile(args.file):
        raise FileNotFoundError(f"{args.file} is not found")
    else:
        config["file"] = args.file

    # Add the remaining args to the dict
    if args.converter == "pdf2jpg":
        if not config["file"].endswith(".pdf"):
            raise TypeError("Incorrect file extension")
        else:
            config["type"] = "pdf2jpg"
            config["initial"] = args.initial
            config["last"] = args.last

    elif args.converter == "jpg2pdf":
        if not config["file"].endswith(".jpg") or config["file"].endswith(".jpeg"):
            raise TypeError("Incorrect file extension")
        else:
            config["type"] = "jpg2pdf"
    
    elif args.converter == "jpgs2pdf":
        ...

    else:
        raise AttributeError

    # Check if the output directory exists
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    config["output"] = args.output

    return config
