import os
from enum import Enum
from time import sleep
from typing import List, Union

from invoke import Collection, task

from scylla_arms.config import ArmsSettings, inject_persistent_models
from scylla_arms.configparser import properties_parser, build_metadata_parser


class Backends(str, Enum):
    aws: str = "aws"
    gce: str = "gce"


class SampleArmsSettings(ArmsSettings):
    backend: Backends
    aws_region: Union[str, List]
    scylla_ami_id: str
    gce_image_db: str = "test_image"
    update_db_packages: str
    scylla_version: str
    scylla_repo: str
    scylla_mgmt_agent_version: str = ""
    scylla_mgmt_address: str

    class Config:
        env_prefix = "SAMPLE_"


@task
def configure(ctx):
    print("preparing configuration")
    settings = SampleArmsSettings()
    print(f"configuration: {settings.dict()}")
    print(
        f'available AWS env vars: {[env for env in os.environ if env.startswith("AWS_")]}'
    )


@task
@inject_persistent_models
def clean(ctx, settings: SampleArmsSettings):
    print("cleaning...")
    print(f"param from configuration: {settings.aws_region}")
    ctx.run("ls scylla_arms")
    sleep(0.5)
    print("cleaning complete!")


@task
@inject_persistent_models
def build(ctx, settings: SampleArmsSettings):
    print("started building...")
    print(f"Setting new context param 'something' to 'test'")
    ctx.persisted.something = "test"
    prop = properties_parser("tasks/sample.properties")
    build_out_file_path = prop.get("buildOutputFile")
    build_metadata_path = prop.get("buildMetadataFile")
    with open(build_out_file_path, "w") as build_out_file:
        ctx.run("lscpu", out_stream=build_out_file)
    res = ctx.run("lscpu --version")
    build_metadata = build_metadata_parser(build_metadata_path, new_file=True)
    build_metadata.set("lscpu-version", res.stdout.strip())
    build_metadata.commit()
    sleep(1)
    print("build complete!")


@task
@inject_persistent_models
def test(ctx, settings: SampleArmsSettings):
    print("started tests...")
    print(f"loaded settings: {settings}")
    assert settings.backend == Backends.aws
    assert ctx.persisted.something == "test"
    sleep(1)
    print("tests complete!")


@task
def package(ctx):
    print("started packaging...")
    sleep(1)
    print("packaging complete!")


@task(configure, clean, build, test, package)
def all_tasks(ctx):
    print("hello world!")


ns = Collection(all_tasks, configure, clean, build, test, package)
