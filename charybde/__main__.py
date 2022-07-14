"""Commands of the charybde package."""
from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    """Create a parser for the main charybde command."""
    parser = ArgumentParser(
        description="Create datasets to train neural nets to count syllables."
    )

    subparsers = parser.add_subparsers(help="Commands", dest="command")

    download_parser = subparsers.add_parser("download", help="Download wiktionaries.")
    download_parser.add_argument(
        "output_dir", help="Path to the directory where files should be downloaded"
    )

    dataset_parser = subparsers.add_parser(
        "dataset", help="Create a dataset out of wiktionaries."
    )
    dataset_parser.add_argument(
        "dumps_folder_path",
        help="Paths to the folder containing the dumps to gather data from.",
    )
    dataset_parser.add_argument(
        "output_path",
        help="Path to the output compressed TSV file. Extension will be added.",
    )
    dataset_parser.add_argument(
        "--langs", nargs="+", help="Langs to consider. Not given = all langs."
    )
    dataset_parser.add_argument(
        "--dumps",
        nargs="+",
        help="Dumps to consider (by language code). Not given = all dumps.",
    )

    filter_parser = subparsers.add_parser(
        "filter", help="Create a dataset out of wiktionaries."
    )
    filter_parser.add_argument(
        "dataset_path",
        help="Path to the dataset to filter.",
    )
    filter_parser.add_argument(
        "filtered_dataset_path",
        help="Path to the output filtered dataset. Extension will be added.",
    )
    return parser


def main() -> None:
    """Perform the argument gathering and orchestration of the main charybde command."""
    parser = create_parser()
    args = parser.parse_args()
    command = args.command
    delattr(args, "command")
    if command == "download":
        from charybde.download import Downloader

        downloader = Downloader(**vars(args))
        downloader.download_all_wiktionaries()
    elif command == "dataset":
        from charybde.dataset import create_csv_dataset_from_dump

        create_csv_dataset_from_dump(**vars(args))
    elif command == "filter":
        from charybde.filter import filter_dataset

        filter_dataset(**vars(args))


if __name__ == "__main__":
    main()
