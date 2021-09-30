import mlflow
import os
import hydra
import wandb
import tempfile
from omegaconf import DictConfig, OmegaConf


_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_model",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
   # "test_model"
]


# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # You can get the path at the root of the MLflow project with this:
    root_path = hydra.utils.get_original_cwd()

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Download step
    
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        
        if "download" in active_steps:

            _ = mlflow.run(
                os.path.join(root_path, "src/get_data"),
                "main",
                parameters={
                    "data_url": config["data"]["data_url"],
                    "artifact_name": "raw_data.zip",
                    "artifact_type": "raw_data",
                    "artifact_decription": "Data as downloaded"
                },
            )


if __name__ == "__main__":
    go()

