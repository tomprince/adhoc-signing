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

# %ARG DOCKER_IMAGE_PACKAGES
RUN ls -l /usr/local/sbin/setup_packages.sh || ls -l /bin/bash || true
RUN /usr/local/sbin/setup_packages.sh $DOCKER_IMAGE_PACKAGES && \
    apt-get update && \
    apt-get install \
      gnupg \
      bzip2 \
      git \
      python3-requests \
      python3-zstandard \
      unzip

# %include taskcluster/run-task/run-task
ADD topsrcdir/taskcluster/scripts/run-task /builds/worker/bin/run-task

# %include taskcluster/run-task/fetch-content
ADD topsrcdir/taskcluster/scripts/fetch-content /builds/worker/bin/fetch-content
