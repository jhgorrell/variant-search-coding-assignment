#
# invitae-hw-variant-search/docker/Makefile ---
#

_default: _docker_build

#####

#
build_cmd+=docker build
build_cmd+=--tag ${INVITAE_VS_DOCKER_IMAGE}
#
build_cmd+=--build-arg "INVITAE_VS_CLIENT=${INVITAE_VS_CLIENT}"
build_cmd+=--build-arg "INVITAE_VS_DEPLOY=${INVITAE_VS_DEPLOY}"
#
build_cmd+=--build-arg "ansible_playbook_extra_args=-vv"
build_cmd+=--file ./Dockerfile
build_cmd+=..

_docker_build:
#
	git gc --aggressive
#
	${build_cmd}
