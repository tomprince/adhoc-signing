# %ARG DOCKER_IMAGE_PARENT
FROM $DOCKER_IMAGE_PARENT

### Add worker user and setup its workspace.
RUN mkdir /builds && \
    groupadd -g 1000 worker && \
    useradd -u 1000 -g 1000 -d /builds/worker -s /bin/bash -m worker && \
    mkdir -p /builds/worker/workspace && \
    chown -R worker:worker /builds

# Declare default working folder
WORKDIR /builds/worker

RUN apt-get update && \
    apt-get install \
      gnupg \
      bzip2 \
      git \
      python3-requests \
      python3-zstandard \
      unzip

# %include taskcluster/scripts/run-task
ADD topsrcdir/taskcluster/run-task/run-task /builds/worker/bin/run-task

# %include taskcluster/scripts/misc/fetch-content
ADD topsrcdir/taskcluster/run-task/fetch-content /builds/worker/bin/fetch-content
