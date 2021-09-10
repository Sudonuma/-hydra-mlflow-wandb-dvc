#!/usr/bin/env python
import argparse
import logging
import pathlib
import wandb
import requests
import tempfile
import os
import gdown


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    logger.info(f"Downloading {args.data_url} ...")
    logger.info("Creating run")
    with wandb.init(job_type="download_data") as run:
        # Download the file streaming and write to open temp file
        file_id = args.data_url.split('/')[-2]
        local_directory = os.path.join("./data/" + args.artifact_name)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.cached_download(url, local_directory, postprocess=gdown.extractall)


        logger.info("Creating artifact")
        artifact = wandb.Artifact(
            name=args.artifact_name,
            type=args.artifact_type,
            description=args.artifact_decription,
            metadata={'original_url': args.data_url}
        )
        # artifact.add_file(fp.name, name=basename)

        logger.info("Logging artifact")
        run.log_artifact(artifact)

        artifact.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a file and upload it as an artifact to W&B", fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--data_url", type=str, help="URL to the input file", required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_decription",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
