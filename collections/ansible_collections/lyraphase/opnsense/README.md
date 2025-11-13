# LyraPhase OPNsense Ansible Collection

The LyraPhase Ansible OPNsense collection includes a variety of Ansible content to help automate the management of OPNsense firewall appliances.

## Support

This Open Source project is not an official Red Hat Ansible [Certified
Content][rh-certified-content], so this collection is **not** entitled to
[support][rh-support] through [Ansible Automation Platform][rh-aap] (AAP).

<!--start requires_ansible-->

## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.19.3**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `lyraphase.opnsense.shell`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.

<!--end requires_ansible-->

## Tested with Ansible

This collection has been tested against OPNsense 24.4.3.

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

It has been tested against the following dependency ansible collection versions:

- `community.general`: `>=10.6.0`
- `ansible.netcommon`: `8.1.0`
- `ansible.utils`: `6.0.0`
- `ansibleguy.opnsense`: `1.2.13`

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

### Supported connections

The OPNsense shell collection supports `network_cli` connections.

It uses the `network_os: lyraphase.opnsense.shell` terminal module to bypass the
initial menu screen shown by `/usr/local/sbin/opnsense-shell`.

## Included content

<!--start collection content-->

### Network terminal plugins

| Name                                         | Description                                                                                   |
| -------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [`lyraphase.opnsense.shell`][opnsense.shell] | Use `ansible.netcommon.network_cli` via `opnsense-shell` to run commands on OPNsense platform |

<!-- TODO -->

### Modules

| Name                                                         | Description                                        |
| ------------------------------------------------------------ | -------------------------------------------------- |
| [`lyraphase.opnsense.shell_command`][opnsense.shell_command] | Run arbitrary commands on OPNsense devices         |
| [`lyraphase.opnsense.facts`][opnsense.facts]                 | Collect facts from remote devices running OPNsense |

<!-- END TODO -->

### Roles

<!-- markdownlint-disable no-inline-html -->

| Name                                         | Description                                                                                             |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| [`lyraphase.opnsense.pkgs`][opnsense.pkgs]   | Install packages on OPNsense devices with `pkg` FreeBSD package manager                                 |
| [`lyraphase.opnsense.users`][opnsense.users] | Add or modify users on remote devices running OPNsense <br/>(depends on: `ansibleguy.opnsense.package`) |

<!--end collection content-->

## Installing this collection

You can install the LyraPhase OPNsense collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install lyraphase.opnsense

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

<!-- markdownlint-disable code-block-style -->

```yaml
---
collections:
  - name: lyraphase.opnsense
```

<!-- markdownlint-enable code-block-style -->

## Using this collection

This collection includes [security resource modules][security-resource-modules].
Similar to [Network resource modules][network-resource-modules] introduced in
Ansible `2.9`

### Using LyraPhase OPNsense Ansible Collection

An example for using this collection to run a raw shell command is as follows:

`inventory.ini` (Note the password should be managed by a [Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) for a production environment.

<!-- markdownlint-disable code-block-style -->

```ini
[opnsense]
opnsense.internal

[opnsense:vars]
ansible_user=root
ansible_ssh_pass={{ opnsense_vault_password }}
ansible_become=true
ansible_become_method=ansible.netcommon.enable
ansible_become_pass=become_password
ansible_connection=ansible.netcommon.network_cli
ansible_network_os=lyraphase.opnsense.shell
# Set according to available OPNsense python package
ansible_python_interpreter=python3.11
```

<!-- markdownlint-enable code-block-style -->

#### Using the modules with Fully Qualified Collection Name (FQCN)

You can either call modules by their Fully Qualified Collection Name (FQCN),
like `lyraphase.opnsense.shell_command`, or you can call modules by their short
name if you list the `lyraphase.opnsense` collection in the playbook's
`collections`, as follows:

<!-- markdownlint-disable code-block-style -->

```yaml
---
- hosts: opnsense
  gather_facts: false
  connection: network_cli

  collections:
    - lyraphase.opnsense

  tasks:
    - name: Get OPNsense version
      register: version_result
      shell_command: &id001
        commands:
          - opnsense-version -v
```

The following example task gathers facts from an OPNsense firewall device, using the FQCN:

```yaml
---
- name: Replace device configurations of listed ACLs with provided configurations
  register: result
  lyraphase.opnsense.facts: &id001
    gather_subset:
      - all
```

<!-- markdownlint-enable code-block-style -->

## Contributing to this collection

We welcome community contributions to this collection. If you find problems,
please open an issue or create a PR against the [LyraPhase OPNsense collection
repository][lyraphase.opnsense]. See the [Ansible Collections Contributor
Guide][ansible-collections-contrib-guide] for complete details.

See the [Ansible Community Guide][ansible-community-guide] for details on
contributing to Ansible.

### Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

Release notes are [available here][changelog].

<!-- ## Roadmap -->

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU Affero General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/agpl-3.0.txt) to see the full text.

[rh-certified-content]: https://catalog.redhat.com/software/search?target_platforms=Red%20Hat%20Ansible%20Automation%20Platform
[rh-support]: https://access.redhat.com/support/
[rh-aap]: https://www.redhat.com/en/technologies/management/ansible
[ansible-collections-contrib-guide]: https://docs.ansible.com/ansible/devel/community/contributions_collections.html
[ansible-community-guide]: https://docs.ansible.com/ansible/latest/community/index.html
[opnsense.shell]: https://github.com/LyraPhase/ansible_opnsense/blob/main/docs/lyraphase.opnsense.shell.md
[opnsense.shell_command]: https://github.com/LyraPhase/ansible_opnsense/blob/main/docs/lyraphase.opnsense.shell_command_module.md
[opnsense.facts]: https://github.com/LyraPhase/ansible_opnsense/blob/main/docs/lyraphase.opnsense.facts_module.md
[opnsense.pkgs]: https://github.com/LyraPhase/ansible_opnsense/blob/main/docs/lyraphase.opnsense.pkgs_role.md
[opnsense.users]: https://github.com/LyraPhase/ansible_opnsense/blob/main/docs/lyraphase.opnsense.users_role.md
[changelog]: https://github.com/LyraPhase/opnsense/blob/main/CHANGELOG.rst
[security-resource-modules]: https://docs.ansible.com/projects/ansible/latest/network/dev_guide/developing_resource_modules_network.html#understanding-network-and-security-resource-modules
[network-resource-modules]: https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html
[lyraphase.opnsense]: https://github.com/LyraPhase/ansible_opnsense
