# Role Name

A simple role to manage OPNsense users + sudoers.
For bootstrapping an OPNsense firewall for Ansible config managment.

## Requirements

This role should first be run in "bootstrap" mode, using the
`bootstrap` tag to first setup your non-root SSH user and `ansible` group.
Afterwards, the `bootstrap` tag can be skipped. It's recommended to run the
bootstrap tasks in either a separate playbook, or by setting using the default
OPNSense user: `root`, & password: `opnsense`.

### Bootstrap Tag Example

    ansible-playbook -i "${REPO_BASE}"/inventory/hosts \
      "${REPO_BASE}"/opnsense-base.yml -vv --tags=bootstrap,never --diff \
      --user=root --ask-pass

## Role Variables

- `lyraphase_opnsense_users_sudoers_path`: The location of `sudoers.d` drop-in directory
   Default: `'/usr/local/etc/sudoers.d'`
- `lyraphase_opnsense_users_ansible_gid`: Group ID for Ansible group.
   [Pick a free(BSD) GID][1]
   Default: `731`

## Dependencies

This role depends on the `collections.general.sudoers` module.
This module is found in the following collectiion:

- community.general

To install this dependency:

    ansible-galaxy collection install community.general

## Example Playbook

There are 2 main scenarios which you could run this role:

1. Bootstrapping
  - In this mode, the goal is to login as the first pre-existing user: `root`,
    to bootstrap the `ansible` group, user, and sudoers permissions.
  - This can be done either with a specialized playbook (example below), or by
    passing CLI flags to
    `ansible-playbook`: `--tags=bootstrap,never --user=root --ask-pass`
  - Passing the `never` tag enables resetting the `root` password to a random value.
2. Normal Config Management
  - On subsequent runs, the playbook should be run in "normal" mode as the
    first config management user (or primary personal Ops/DevOps user)
  - The reason for this modality is to enable security & auditing for subsequent
    actions performed on the system post-bootstrap.
  - In this mode the playbook will add other users and groups to the system,
    as defined in the role's configuration variables.

### Bootstrap Playbook Example

    - hosts: opnsense
      user: root
      gather_facts: no
       
      roles:
        - role: lyraphase.opnsense_users
          tags:
            - { role: opnsense_users, lyraphase_opnsense_users_ansible_gid: 777 }

To run only the bootstrap tasks, pass the `--tags=bootstrap,never` CLI flag to Ansible

     ansible-playbook bootstrap-play.yml --tags "bootstrap,never"

> [!CAUTION]
> **Note:** The `never` tag enables running the "Reset root password" task!
> 
> Ensure that you save the `root` user's new password that will be output from
> this task, because it will only be shown once.

## License

AGPLv3

## Author Information

James Cuzella @trinitronx

[1]: https://cgit.freebsd.org/ports/tree/GIDs

