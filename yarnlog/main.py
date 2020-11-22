import datetime
import html
import os

import fire
import requests
from hurry.filesize import size


def extract(text: str) -> str:
    """Extract content inside pre tag."""
    PRE_START = "<pre>"
    PRE_END = "</pre>"
    try:
        p_start = text.index(PRE_START)
        p_end = text.index(PRE_END)
        return html.unescape(text[p_start + len(PRE_START) : p_end])
    except ValueError as e:
        print(e)
        return ""


def download_and_extract(yarn_url: str) -> str:
    """Download and extract log content from YARN."""
    print(f"downloading from {yarn_url}")
    r = requests.get(yarn_url)
    output = r.text
    if "<pre>" in r.text:
        output = extract(r.text)
    original_url = "EXTRACTED FROM {}".format(yarn_url)
    output = original_url + "\n" + output
    return output


def save_file(output: str, output_file: str):
    """Save output to file."""
    with open("{}".format(output_file), "w+") as f:
        f.write(output)
    print("output: {}".format(output_file))
    s = os.path.getsize(output_file)
    print("line count: {}".format(output.count("\n")))
    print("file size: {}".format(size(s)))


def pipeline(yarn_url):
    """Run the whole yarnlog pipeline."""
    output = download_and_extract(yarn_url)
    output_filename = "yarnlog_" + datetime.datetime.now().strftime(
        "%Y_%m_%d_%H%M%S__%f"
    )
    save_file(output, output_filename)


def main():
    fire.Fire(pipeline)


if __name__ == "__main__":
    main()
