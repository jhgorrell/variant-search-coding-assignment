#
# invitae-hw-variant-search/docker/Dockerfile ---
#

FROM ubuntu:20.04

SHELL ["bash","-c"]

###

ARG ansible_playbook_extra_args=

ARG INVITAE_VS_DIR=/opt/invitae-hw-variant-search
ENV INVITAE_VS_DIR=${INVITAE_VS_DIR}

ARG INVITAE_VS_VE_DIR=${INVITAE_VS_DIR}/ve
ENV INVITAE_VS_VE_DIR=${INVITAE_VS_VE_DIR}

ARG TZ=America/Edmonton
ENV TZ=${TZ}

# This is a subset of the env vars from hba-setup.
# The "PG*" vars and some others are required to be passed
# in with "--env VAR"
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENV INVITAE_VS_SYSTEM=docker

ENV PATH=${INVITAE_VS_DIR}/bin:${INVITAE_VS_VE_DIR}/bin:${PATH}

WORKDIR ${INVITAE_VS_DIR}

### pass: init

RUN apt-get update -y

RUN DEBIAN_FRONTEND=noninteractive \
        apt-get install -y \
        ansible \
        aptitude \
        make \
        python3-apt \
        python3-venv \
        sqlite3 \
        tzdata

### pass: source

COPY ./ ./

RUN ANSIBLE_SYSTEM_WARNINGS=False \
        ansible-playbook \
        ${ansible_playbook_extra_args} \
        --inventory "localhost," \
        --connection "local" \
       ./ansible/docker-install/docker-install-play.yml

### pass: brand the image.
### do this at the end so we dont invalidate the cache.

ARG INVITAE_VS_CLIENT
ENV INVITAE_VS_CLIENT=${INVITAE_VS_CLIENT}

ARG INVITAE_VS_SITE
ENV INVITAE_VS_SITE=${INVITAE_VS_SITE}

ARG INVITAE_VS_DEPLOY
ENV INVITAE_VS_DEPLOY=${INVITAE_VS_DEPLOY}

# Local Variables:
# mode: dockerfile
# End:
