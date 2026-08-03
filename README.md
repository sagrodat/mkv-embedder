# MKV Embedder

MKV Embedder is a simple command-line tool designed to embed additional information into MKV video files and extract it later. The main goal is to allow MKV files to contain more than just video data - now they can hold extra files (currently ZIP attachments).

## Features

- **Embed Attachments:** Insert a ZIP file as an attachment into an MKV video.
- **Extract Attachments:** Retrieve the embedded ZIP file from an MKV video.
- **Custom Extraction Path:** Extract using the original filename or specify a custom output file or directory.
- **Testing Samples:** The `sample_videos` folder contains small MKV snippets (around 5 seconds each and under 500KB) that you can use for testing or future storage.

# Installation

## 1. Clone the Repository:

```bash
git clone https://github.com/sagrodat/mkv_embedder.git
cd mkv_embedder
```

## 2. Install Dependencies:

- This tool requires Python 3.
- MKVToolNix utilities are required:
    - `mkvmerge`
    - `mkvextract`
    - `mkvinfo`


### Linux

Install MKVToolNix system-wide using your package manager.

Ubuntu/Debian:

```bash
sudo apt install mkvtoolnix
````

Other distributions should use their respective package manager.

The application will automatically use the system-installed MKVToolNix utilities.

*Or follow install instructions from the official webpage https://mkvtoolnix.org/*

### Windows

Install MKVToolNix manually from the official website - https://mkvtoolnix.org/ 

Place the executable files inside the `bin` catalog.

The required files are:

```
bin/
├── mkvmerge.exe
├── mkvextract.exe
└── mkvinfo.exe
```


# Usage

The tool operates via the command line with two main commands: `embed` and `extract`.

## Embedding an Attachment

To embed a ZIP file into an MKV video, run:

```bash
python mkv_embedder.py embed -i path/to/input.mkv -a path/to/attachment.zip -o path/to/output.mkv
```

* `-i`, `--input`: Path to the input MKV video file.
* `-a`, `--attachment`: Path to the ZIP file to embed.
* `-o`, `--output`: Path where the output MKV (with the embedded attachment) will be saved.

## Extracting an Attachment

Extract using the original embedded filename:

```bash
python mkv_embedder.py extract -i path/to/input_with_attachment.mkv
```

Extract to a specific file:

```bash
python mkv_embedder.py extract -i path/to/input_with_attachment.mkv -o extracted.zip
```

Extract into a directory:

```bash
python mkv_embedder.py extract -i path/to/input_with_attachment.mkv -o output_folder
```

* `-i`, `--input`: Path to the MKV file from which to extract the attachment.
* `-o`, `--output`: (Optional) Output file or directory. If omitted, the original attachment filename is used.

## Notes

* Only ZIP attachments are currently supported.
* If the required MKVToolNix utilities are not available, the tool will exit with an error message.
* Detailed error messages are provided to help diagnose any issues during embedding or extraction.

## Acknowledgements

This tool is made possible thanks to [MKVToolNix](https://mkvtoolnix.org/). Its excellent and well-documented suite of utilities provides all of the underlying functionality used by this project. This script simply offers a more focused and convenient interface for embedding and extracting MKV attachments.