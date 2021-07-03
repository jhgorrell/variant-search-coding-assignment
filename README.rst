invitae-hw-variant-search/README
==================================================

Submission for the invitate homework.

Links:

- Server: https://invitae-vs-dev.home.mahalito.net/
- Repo: https://github.com/jhgorrell/invitae-hw-variant-search
- Repo: http://gitlab-1.home.mahalito.net/harley/invitae-hw-variant-search
- Jenkins: http://jenkins-1.home.mahalito.net/job/invitate/
- Docs: None!
- Original README: `original/README.md <original/README.md>`_

SPDX-License-Identifier: ``CC-BY-NC-3.0``

Quickstart / devs
--------------------------------------------------

::

    git clone https://github.com/jhgorrell/invitae-hw-variant-search.git
    cd invitae-hw-variant-search
    source ./setup.env

    # dev
    make _ve_rebuild
    make _server_run_flask

    # deploy (works on my home systems.)
    make _docker_build _deploy_server ; sudo systemctl restart nginx


Discussion
--------------------------------------------------

- This project was generated with `cookiecutter
  <https://cookiecutter.readthedocs.io/>`_ and then the
  editied into its final form.  The parts which werent
  needed for this repo were removed.

- The app is a single page, without react, the backend is
  flask and the DB is sqlalchemy & sqlite. (sqlite as I want
  the reviewers to be able to run locally.)

- Did a simple native javascript as my React is rusty
  and wanted to keep the time down.

- I like to keep the server as a thin veneer over
  the core - this helps with code resue (cli vs web) and
  keeps testing simplier.

- Skipped the unit tests - the utility app is a smoke test
  which I used to get the SQL working; If you look at my
  other homework, you can check out that unit testing.

What is extra
--------------------------------------------------

- Ansible!
- Docker!

What was left out
--------------------------------------------------

- Error checking!
- DB migrations!
- Kubernetes!
- Sphinx docs!
- Testing!
