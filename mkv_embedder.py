import argparse
import subprocess
import os
import sys
import shutil
import platform


def get_exe_path(exe_name):
    if platform.system() == "Windows":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(base_dir, "bin", exe_name + ".exe")

        if not os.path.exists(exe_path):
            raise FileNotFoundError(
                f"{exe_name}.exe not found in bin directory."
            )

        return exe_path

    elif platform.system() == "Linux":
        exe_path = shutil.which(exe_name)

        if exe_path:
            return exe_path

        raise FileNotFoundError(
            f"{exe_name} was not found. Install MKVToolNix first.\n"
            f"Ubuntu/Debian: sudo apt install mkvtoolnix"
        )

    else:
        raise OSError(
            f"Unsupported operating system: {platform.system()}"
        )


def get_mkvmerge_path():
    return get_exe_path("mkvmerge")


def get_mkvextract_path():
    return get_exe_path("mkvextract")


def get_mkvinfo_path():
    return get_exe_path("mkvinfo")


def add_attachment_to_mkv(input_mkv, attachment_path, output_mkv, mime_type="application/zip"):
    mkvmerge_exe = get_mkvmerge_path()

    command = [
        mkvmerge_exe,
        "-o",
        output_mkv,
        "--attach-file",
        attachment_path,
        "--attachment-mime-type",
        mime_type,
        input_mkv
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Attachment added successfully. Output file: {output_mkv}")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running mkvmerge:", e)
        sys.exit(1)


def get_attachment_name_from_mkv(input_mkv):
    mkvinfo_exe = get_mkvinfo_path()

    try:
        result = subprocess.check_output(
            [mkvinfo_exe, input_mkv],
            universal_newlines=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print(e.output if e.output else str(e))
        sys.exit(1)

    attachment_name = None

    for line in result.splitlines():
        line = line.strip()

        if "File name:" in line:
            _, _, potential_name = line.partition(": ")

            if potential_name.endswith(".zip"):
                attachment_name = potential_name

    if attachment_name is None:
        print("Attachment name not found in MKV file.")
        sys.exit(1)

    return attachment_name


def extract_attachment_from_mkv(input_mkv, output_path=None):
    attachment_name = get_attachment_name_from_mkv(input_mkv)
    mkvextract_exe = get_mkvextract_path()

    if output_path:
        if os.path.isdir(output_path):
            output_file = os.path.join(output_path, attachment_name)
        else:
            output_file = output_path
    else:
        output_file = attachment_name

    command = [
        mkvextract_exe,
        "attachments",
        input_mkv,
        f"1:{output_file}"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Attachment extracted successfully as {output_file}")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running mkvextract:", e)
        sys.exit(1)


def embed_attachment(args):
    add_attachment_to_mkv(
        args.input,
        args.attachment,
        args.output
    )


def extract_attachment(args):
    extract_attachment_from_mkv(
        args.input,
        args.output
    )


def main():
    parser = argparse.ArgumentParser(
        description="Tool for embedding and extracting ZIP attachments in MKV files."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    embed_parser = subparsers.add_parser(
        "embed",
        help="Embed a file into an MKV."
    )

    embed_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input MKV file."
    )

    embed_parser.add_argument(
        "-a",
        "--attachment",
        required=True,
        help="ZIP file to embed."
    )

    embed_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output MKV file."
    )

    embed_parser.set_defaults(
        func=embed_attachment
    )

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract the attachment from an MKV."
    )

    extract_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input MKV file."
    )

    extract_parser.add_argument(
        "-o",
        "--output",
        help="Output file or directory."
    )

    extract_parser.set_defaults(
        func=extract_attachment
    )

    args = parser.parse_args()

    try:
        args.func(args)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except OSError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()