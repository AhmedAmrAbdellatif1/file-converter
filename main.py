from args_parser import args_parser
import convert

"""_dependencies_
    pip install pdf2image
    pip install fpdf2
    pip install --upgrade Pillow
"""


# Usage
def main() -> None:

    configurations: dict = args_parser()
    match configurations["type"]:
        case "pdf2jpg":
            convert.pdf_to_jpg(
                configurations["file"],
                configurations["output"],
                configurations["initial"],
                configurations["last"],
            )
        case "jpg2pdf":
            convert.jpg_to_pdf(configurations["file"], configurations["output"])


if __name__ == "__main__":
    main()
