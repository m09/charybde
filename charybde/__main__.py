"""Commands of the charybde package."""
from argparse import ArgumentParser

from charybde.dataset import create_csv_dataset_from_dump
from charybde.download import Downloader


def create_parser() -> ArgumentParser:
    """Create a parser for the main charybde command."""
    parser = ArgumentParser("Create datasets to train neural nets to count syllables.")
    subparsers = parser.add_subparsers(help="Commands", dest="command")
    download_parser = subparsers.add_parser("download", help="Download wiktionaries.")
    download_parser.add_argument("output_dir", help="Path to the directory where files should be "
                                                    "downloaded")
    dataset_parser = subparsers.add_parser("dataset", help="Create a dataset out of wiktionaries.")
    dataset_parser.add_argument("dumps_folder_path",
                                help="Paths to the folder containing the dumps to gather data "
                                     "from.")
    dataset_parser.add_argument("output_path", help="Path to the output compressed TSV file. "
                                                    "Extension will be added.")
    dataset_parser.add_argument("--langs", nargs="*", help="Langs to consider. Empty = all langs.")
    return parser


def main() -> None:
    """Perform the argument gathering and orchestration of the main charybde command."""
    parser = create_parser()
    args = parser.parse_args()
    command = args.command
    delattr(args, "command")
    if command == "download":
        downloader = Downloader(**vars(args))
        downloader.download_all_wiktionaries()
    elif command == "dataset":
        create_csv_dataset_from_dump(**vars(args))


if __name__ == "__main__":
    main()
