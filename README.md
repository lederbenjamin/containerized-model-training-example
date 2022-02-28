## Answers
### What choices did you have to make?
  + Multistage vs Single
    + If certain folders are copied to the next build cycle, multistage builds can allow for faster image builds and lighter containers;
    + However, given that gnupg2 libgpgme-dev swig are all required at runtime, copying the entire file system to the next cycle would be counterproductive.
    + As such, a single build cycle is sufficient
  + Poetry over Pip
    + Pip
      + Maintaining pip based files is a time intensive manual process for large projects.
      + This is especially true when version changes are frequent and in high volume 
    + Poetry
      + pyproject.toml is your one-stop central configuration file 
      + This file allows for management of dependencies, configurations, project info and more
      + poetry.lock contains an exact package hash for added security during package installation 
  + sleep() is unsafe
    + Problem
      + The model requires time for training and packaging
      + As such, how should model_train.sh handle this wait period?
    + sleep 
      + The easy solution would be a hardcoded sleep
      + However, what if the model takes longer than the hardcoded time? 
      + Or, what if the model finishes considerably earlier?
      + Whether your concern is errors or inefficiency, hardcoded values are almost never viable
    + is_ready.sh
      + A dynamic solution allows for the host to communicate with the container to determine readiness
      + To achieve this, we include a script as a part of our image
      + This script can be called via a docker exec command to determine if the tar file is ready
### Are there particular conventions that you followed, that you consider good practice? Why?
  + .dockerignore
    + We need images to be built as fast and as lightweight as possible
    + One step we can take is to exclude irrelevant files 
    + To do this without restructuring our source code, we use a .dockerignore file. 
    + This file offers file exclusion functionality similar to .gitignore files.
  + Limiting layers
    + We could have a 1:1 RUN or COPY command for every file / installation necessary 
    + However, this would greatly increase the number of layers in our image
    + More layers, means a slower image build and this is not ideal
    + The solution is to chain these commands as a single layer, within reason
  + Handling multi-line arguments
    + We sorted the arguments alphanumerically
    + This helps...
      + To avoid duplication of packages
      + Make updates much easier 
      + Make PRs easier to read and review
### What standardization issues are addressed by a dockerized training environment?
  + The problem with VMs...
    + When developing any ml application / service, a 1:1 ratio of virtual machines (VMs) to services must exist. 
    + Even if a service is not up, that VM will still be consuming hardware resources and disk space
    + Also, each VM needs an OS, libraries, and binaries to support your ml service
    + This is wasteful and limiting with respect to scalability
    + It also creates barriers to environment migration i.e. shipping the model
  + Docker, the god emperor
    + Resource Efficiency 
      + When a container is not running, the remaining resources become shared resources and are accessible to all other containers in the pod. 
      + Additionally, an OS is not required for containerized services further lowering overhead. 
    + Ship Anywhere
      + Most importantly, Docker allows us to easily reproduce the training environment
      + Specifically, Docker packages code and dependencies into a portable solution that will run on any operating systems or hardware.
      + This allows models to be developed on a local machine and then easily shipped to internal or external environments
### What does requirements.txt accomplish? 
  + This is pip's configuration file for listing dependencies
### Are there any shortcomings of using pip/requirements.txt to specify package versions? 
  + Versioning on projects with large dependency trees quickly becomes difficult to read and change if you're stuck with pip
### What alternative methods are there?
  + Poetry is pure... poetry

# Challenge Description

Scenario: you work for a sports journalism website that is implementing a text classification model. The model
classifies which sport a piece of text is about. The data science team has implemented model training code and saved a
serialized model.

Training and saving the model on personal development environments has caused some inconsistencies. The infra team is
responsible for standardizing the training environment using Docker.

***

+ Challenge prereqs: [Docker](https://www.docker.com/)

Your task is to standardize the training environment for a machine learning model.

We are providing code that trains the model. Machine learning tasks like model validation and hyperparameter tuning are
not important for this challenge. The provided script loads its own data, trains the model, and uses Kensho's
open-source serialization library, `special_k`, to serialize the model securely. The script takes one argument: the
location at which the model should be stored.

[special_k](https://github.com/kensho-technologies/special_k/blob/master/docs/usage.md#serializing-and-deserializing-models)
uses GPG keys to allow downstream users to verify the model's origin. Although not a good security practice, we are
providing both public and private keys for this challenge for convenience in the `/gnupg` directory. Make sure to
read `special_k`'s documentation for installation instructions.

Tasks for completing this challenge:

+ Write a Dockerfile that uses the python training script (`train.py`) to train and serialize the model. We have
  provided a starter Dockerfile for you.
+ Write a bash script which will execute the model training and serialization using the Dockerfile. After the script has
  run, there should be a `models` directory in the `challenge_1` folder that contains the trained model tarball.
+ Specify versions of python packages in requirements.txt. If you know of other python package management solutions,
  feel free to implement those.

For full credit, ensure that your code runs, including the python model serialization script, the Dockerfile and the
bash script invoking the Dockerfile.

Address the following prompts in 1-3 paragraphs:

+ Describe your solution: what choices did you have to make? Are there particular conventions that you followed, that
  you consider good practice? Why?
+ What standardization issues are addressed by dockerizing a training environmnent?
+ What does requirements.txt accomplish? Are there any shortcomings of using pip/requirements.txt to specify package
  versions? What alternative methods are there?
