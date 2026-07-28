import tempfile
from pathlib import Path
from pprint import pformat

import click
import yaml

from logger import logger
from books_actions import BooksActions, tmp_dir
from PdfManifestEntry import BooksLib


def load_books_lib(
    yaml_path: str,
    tmp_path: str = None,
    update_yaml_info: bool = False,
    copy_pdfs: bool = False,
    move_no_info: bool = False,
    sanitize_didier: bool = False,
    fitz_didier: bool = False,
    sanitize_info: bool = False,
    print_first: bool = False,
):
    """Load books library and perform requested operations."""
    logger.info(f"sanitize_info={sanitize_info}")
    books_lib: BooksLib = BooksLib.from_yaml_path(yaml_path)
    if not tmp_path:
        tmp_path = tmp_dir()
    books_lib.tmp_path = tmp_path
    logger.info(f"loaded {pformat(books_lib)}")
    print()
    
    # Create BooksActions instance and perform operations
    actions = BooksActions(books_lib)
    actions.load_books_lib_operations(
        tmp_path=tmp_path,
        update_yaml_info=update_yaml_info,
        copy_pdfs=copy_pdfs,
        move_no_info=move_no_info,
        sanitize_didier=sanitize_didier,
        fitz_didier=fitz_didier,
        sanitize_info=sanitize_info,
        print_first=print_first,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


@click.command()
@click.argument("yaml_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--tmp-path", type=click.Path(path_type=Path), help="Optional temporary path.")
@click.option("--copy-pdfs", is_flag=True, default=False, help="copy pdf files from input_files to tmp")
@click.option("--update-yaml-info", is_flag=True, default=False, help="copy pdf files from input_files to tmp")
@click.option("--move-no-info", is_flag=True, default=False, help="move pdf files from tmp if no info")
@click.option("--sanitize-didier", is_flag=True, default=False, help="sanitize and move pdf by didier finds")
@click.option("--fitz-didier", is_flag=True, default=False, help="fitz and move pdf by didier finds")
@click.option("--sanitize-info", is_flag=True, default=False, help="sanitize info into pdf")
@click.option(
    "--print-first",
    "print_first",
    is_flag=True,
    default=False,
    help="Print first entry from yaml.",
)
def main(
    yaml_path: str,
    tmp_path: str,
    update_yaml_info: bool,
    copy_pdfs: bool,
    move_no_info: bool,
    sanitize_didier: bool,
    fitz_didier: bool,
    sanitize_info: bool,
    print_first: bool,
) -> None:
    load_books_lib(
        yaml_path,
        tmp_path=tmp_path,
        update_yaml_info=update_yaml_info,
        copy_pdfs=copy_pdfs,
        move_no_info=move_no_info,
        sanitize_didier=sanitize_didier,
        fitz_didier=fitz_didier,
        sanitize_info=sanitize_info,
        print_first=print_first,
    )


if __name__ == "__main__":
    main()
# /bin/python yaml_actions.py ~/shared/gitlab_books/output.yaml --print-first
# /bin/python yaml_actions.py ~/shared/gitlab_books/output.yaml --tmp-path=/tmp/stam
# /bin/python yaml_actions.py ~/shared/gitlab_books/output.yaml  --copy-pdfs
# /bin/python yaml_actions.py copied.yml --tmp-path=/tmp/tmpijmg7hk2 --update-yaml-info
# /bin/python yaml_actions.py  files_info.yaml --tmp-path=/home/sd/tmp/1-sanitized2/ --move-no-info
# python yaml_actions.py  files_info.yaml --tmp-path=/home/sd/tmp/one_file --sanitize-didier"
# python yaml_actions.py  files_info.yaml --tmp-path=/home/sd/tmp/sanitized --sanitize-info"
