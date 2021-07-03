#
# invitae-hw-variant-search/ansible/Makefile ---
#
# Ansible stuff to deploy our server and stuff.
#

_default:

#####

# Could have more than one.
inventory_yml:=./deploy-server/${INVITAE_VS_CLIENT}-${INVITAE_VS_DEPLOY}-inv.yml

ansible_playbook_exe:=${INVITAE_VS_VE_DIR}/bin/ansible-playbook

args_ansible+=-vv
args_ansible+=--inventory ${inventory_yml}
args_ansible+=-e ansible_python_interpreter=/usr/bin/python3

#####

${ansible_playbook_exe}:
	pip3 install ansible

_deploy_server: | ${ansible_playbook_exe}
	${ansible_playbook_exe} \
	  ${args_ansible} \
	  ./deploy-server/deploy-server-play.yml
