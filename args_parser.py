import argparse
import glob
import os


class Parser:
    def __init__(self) -> None:
        # Initialize the argument parser with a description for the CLI tool
        self.parser = argparse.ArgumentParser(description="File type conversion")

        # Define subparsers for different conversion types (pdf2jpg, jpg2pdf)
        self.subparsers = self.parser.add_subparsers(
            dest="converter", required=True, title="Available conversion types"
        )

        # Parser for pdf2jpg conversion
        self.parser_pdf2jpg = self.subparsers.add_parser(
            name="pdf2jpg",
            help="Convert a PDF file to JPEG images",
            epilog="Example usage: python main.py pdf2jpg -f document.pdf -o /path/to/output",
        )
        # Argument for input PDF file
        self.parser_pdf2jpg.add_argument(
            "-f",
            "--file",
            metavar="filename",
            help="Path to the PDF file that will be converted to JPEG images (required)",
            type=str,
            required=True,
        )
        # Argument for output directory (optional, default: current directory)
        self.parser_pdf2jpg.add_argument(
            "-o",
            "--output",
            metavar="directory",
            help="Directory where the converted JPEG images will be saved (default: current working directory)",
            type=str,
            default=os.getcwd(),
        )
        # Argument for specifying the initial page number (optional)
        self.parser_pdf2jpg.add_argument(
            "-i",
            "--initial",
            metavar="page-number",
            help="Starting page number for conversion (default: first page)",
            type=int,
            default=None,
        )
        # Argument for specifying the last page number (optional)
        self.parser_pdf2jpg.add_argument(
            "-l",
            "--last",
            metavar="page-number",
            help="Ending page number for conversion (default: last page of the PDF)",
            type=int,
            default=None,
        )

        # Parser for jpg2pdf conversion
        self.parser_jpg2pdf = self.subparsers.add_parser(
            name="jpg2pdf",
            help="Convert one or more JPEG images into a PDF",
        )
        # Create a mutually exclusive group for --files and --path
        self.exgroup_jpg2pdf = self.parser_jpg2pdf.add_mutually_exclusive_group(
            required=True
        )

        # Argument for input JPEG file(s)
        self.exgroup_jpg2pdf.add_argument(
            "-f",
            "--files",
            metavar="filename",
            help="The name of the JPEG file or a list of JPEG files to be converted to a single PDF",
            nargs="+",
            type=str,
        )
        # Argument for input JPEG files path
        self.exgroup_jpg2pdf.add_argument(
            "-p",
            "--path",
            metavar="directory",
            help="The path of the JPEG files to be converted to a single PDF",
            type=str,
        )
        # Argument for output directory (optional, default: current directory)
        self.parser_jpg2pdf.add_argument(
            "-o",
            "--output",
            metavar="directory",
            help="Directory where the generated PDF will be saved (default: current working directory)",
            type=str,
            default=os.getcwd(),
        )

        # Add parser for the mergePDFs functionality
        self.parser_mergePDFs = self.subparsers.add_parser(
            name="mergePDFs",
            help="Merge multiple PDF files into a single PDF",
        )
        # Create a mutually exclusive group for --files and --path
        self.exgroup_mergePDFs = self.parser_mergePDFs.add_mutually_exclusive_group(
            required=True
        )
        # Argument for specifying the input PDF files to be merged
        self.exgroup_mergePDFs.add_argument(
            "-f",
            "--files",
            metavar="filename",
            help="List of PDF files to be merged into a single PDF (required)",
            nargs="+",  # Allows multiple files to be passed as a list
            type=str,
        )
        # Argument for input JPEG files path
        self.exgroup_mergePDFs.add_argument(
            "-p",
            "--path",
            metavar="directory",
            help="The path of the JPEG files to be converted to a single PDF",
            type=str,
        )
        # Argument for specifying the output directory where the merged PDF will be saved
        self.parser_mergePDFs.add_argument(
            "-o",
            "--output",
            metavar="directory",
            help="Directory where the generated merged PDF will be saved (default: current working directory)",
            type=str,
            default=os.getcwd(),  # Default to the current working directory if not provided
        )

        # Parser for compressPDF conversion
        self.parser_compressPDF = self.subparsers.add_parser(
            name="compressPDF",
            help="Compress a PDF file to reduce its size",
        )
        # Argument for input PDF file
        self.parser_compressPDF.add_argument(
            "-f",
            "--file",
            metavar="filename",
            help="Path to the PDF file that will be compressed",
            type=str,
            required=True,
        )
        # Argument for output directory (optional, default: current directory)
        self.parser_compressPDF.add_argument(
            "-o",
            "--output",
            metavar="directory",
            help="Directory where the compressed PDF will be saved (default: current working directory)",
            type=str,
            default=os.getcwd(),
        )

    def parse(self) -> None:
        # Parse the command-line arguments provided by the user
        self.args = self.parser.parse_args()
        # Validate and process the parsed arguments
        self.checker()

    def checker(self) -> None:
        # Validation and setup for pdf2jpg conversion
        if self.args.converter == "pdf2jpg":
            if not os.path.isfile(self.args.file) or not self.args.file.endswith(
                ".pdf"
            ):
                raise FileNotFoundError(f"{self.args.file} is not found")
            else:
                self.file = self.args.file
                self.type = "pdf2jpg"
                self.initial = self.args.initial
                self.last = self.args.last

        # Validation and setup for jpg2pdf conversion
        elif self.args.converter == "jpg2pdf":
            if self.args.files:
                for file in self.args.files:
                    if not os.path.isfile(file) or not file.endswith(".jpg"):
                        raise FileNotFoundError(f"{file} is not found")
                self.files = self.args.files

            elif self.args.path:
                self.args.path = self.args.path.replace('/','\\')
                self.files = glob.glob(f"{self.args.path}\\*.jpg")
            
            else:
                raise AttributeError(
                    "Please specify either the list of JPEGs or the path contains them"
                )

            self.type = "jpg2pdf"

        # Validation and setup for mergePDFs conversion
        elif self.args.converter == "mergePDFs":
            
            if self.args.files:
                for file in self.args.files:
                    if not os.path.isfile(file) or not file.endswith(".pdf"):
                        raise FileNotFoundError(f"{file} is not found")
                self.files = self.args.files
                    
            elif self.args.path:
                self.args.path = self.args.path.replace('/','\\')
                self.files = glob.glob(f"{self.args.path}\\*.pdf")

            self.type = "mergePDFs"

        # Validation and setup for compressPDF conversion
        elif self.args.converter == "compressPDF":

            if not os.path.isfile(self.args.file) or not self.args.file.endswith(
                ".pdf"
            ):
                raise FileNotFoundError(f"{self.args.file} is not found")

            self.file = self.args.file
            self.type = "compressPDF"

        else:
            raise AttributeError

        # Create output directory if it doesn't exist
        if not os.path.exists(self.args.output):
            os.mkdir(self.args.output)
        self.output = self.args.output
