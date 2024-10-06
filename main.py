from args_parser import *
from convert import *

"""_dependencies_
    pip install pdf2image
    pip install fpdf2
    pip install --upgrade Pillow
    pip install PyPDF2
    pip install tqdm
"""


# Main function to handle the file conversion based on parsed arguments
def main() -> None:

    # Initialize and parse the command-line arguments
    parser = Parser()
    parser.parse()

    # Execute the appropriate conversion based on the parsed type
    match parser.type:
        case "pdf2jpg":
            pdf_to_jpg(
                pdf_file=parser.file,
                output_dir=parser.output,
                first_page=parser.initial,
                last_page=parser.last,
            )
        case "jpg2pdf":
            jpg_to_pdf(images=parser.files, output_dir=parser.output)

        case "mergePDFs":
            merge_pdfs(
                pdfs=parser.files,
                output_dir=parser.output,
            )
        
        case "splitPDF":
            split_pdf(
                pdfs=parser.files,
                output_dir=parser.output,
            )

        case "compressPDF":
            compress_pdf(
                pdf=parser.file,
                output_dir=parser.output,
            )

        case _:
            raise AttributeError


# Entry point for the script
if __name__ == "__main__":
    main()
