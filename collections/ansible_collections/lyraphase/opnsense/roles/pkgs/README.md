# Role Name

A simple role to manage OPNsense Packages.
Install packages on an OPNsense firewall for Ansible config managment.

## Requirements

- An initial ansible bootstrap user should already be installed.
- Dependencies should be installed

## Role Variables

- `opnsense_pkgs_list`: The list of packages to install
   Default: `none`

## Dependencies

This role depends on the `collections.general.sudoers` module.
These modules are found in the following collectiions:

- community.general
- ansibleguy.opnsense

To install this dependency:

    ansible-galaxy collection install community.general
    ansible-galaxy collection install ansibleguy.opnsense

## Example Playbook

This example playbook installs the `lsblk` and `rsync` packages to `opnsense`
hosts.  The playbook is run as `opnsense-user`.

    - name: Install OPNsense packages
      hosts: opnsense
      user: opnsense-user
      gather_facts: false
    
      roles:
        - role: lyraphase.opnsense.opnsense_pkgs
          opnsense_pkgs_list: ['lsblk', 'rsync']
          tags: packages

## License

AGPLv3

## Author Information

James Cuzella @trinitronx
