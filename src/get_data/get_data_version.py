#!/usr/bin/env python
import argparse
import logging
import pathlib
import wandb
import requests
import tempfile
import os
# import gdown
import yaml

# step should be in the preprocess data or in the check data

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


# Get url from DVC
import dvc.api
from dvc.repo import Repo


def go(args):

    # logger.info(f"Downloading {args.data_url} ...")
    logger.info("Creating run")

    data_url = dvc.api.get_url(
        path='/home/hydra-mlflow-wandb-dvc/src/get_data/data',
        repo=args.repo,
        rev='9cb5b22db42ed008416f443eb6a1dabab16d6af1'
    )

    logger.info("pulling data with DVC")
    repo = Repo(".")
    repo.pull()


    with wandb.init(job_type="change_data_version") as run:
        with dvc.api.open('/home/hydra-mlflow-wandb-dvc/src/get_data/data.dvc') as fd:
        # Download the file streaming and write to open temp file
        # file_id = args.data_url.split('/')[-2]
        # local_directory = os.path.join("./data/" + args.artifact_name)
        # url = f"https://drive.google.com/uc?id={file_id}"
        # gdown.cached_download(url, local_directory, postprocess=gdown.extractall)
            
            dataconfig = yaml.safe_load(fd)

            logger.info("Creating artifact")
            artifact = wandb.Artifact(
                name=args.artifact_name,
                type=args.artifact_type,
                description=args.artifact_decription,
                metadata={'original_url': data_url, 'version': args.version}
            )
            artifact.add_file(fd.name, name='data.dvc')
            # artifact.add_file(fp.name, name=basename)


            logger.info("Logging artifact")
            run.log_artifact(artifact)

            artifact.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a specifec version of your data and upload it as an artifact to W&B", fromfile_prefix_chars="@"
    )
# check how to do it in a remote storage (without the path, with a url) (ambe you wont need it, you can download the latest version with dvc pull then download the the specific version with this script (as all git commits should be available in your local machine))
    parser.add_argument(
        "--data_path", type=str, help="path to data to your data",  default="/home/hydra-mlflow-wandb-dvc/src/get_data/"
    )

    parser.add_argument(
        "--repo", type=str, help="repository",  default="https://github.com/Sudonuma/hydra-mlflow-wandb-dvc.git" 
    )

    parser.add_argument(
        "--version", type=str, help="version",  default="v2"
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact",  default="versionv2"
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact",  default='raw_data'
    )

    parser.add_argument(
        "--artifact_decription",
        type=str,
        help="Description for the artifact",
        required=True, default="data version"
    )

    args = parser.parse_args()

    go(args)
