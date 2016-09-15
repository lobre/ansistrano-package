# Ansistrano Package Role

This ansible role has been created in complement of Ansistrano deploy scripts.
You can find them here: [Ansistrano](https://github.com/ansistrano)

This role creates a package locally from a git repository. Then, this package will be uploaded with Ansistrano deploy role and its rsync strategy.

It has been created because the remote server has not always access to the git repository. So for this case, the git repository is hit from the local machine. The package is then created and arranged locally.

The variables are fully compatible with Ansistrano variables.

## Installation

In order to install Ansistrano package, deploy and rollback roles you can create a `requirements.yml` file for instance.

    # requirements.yml
    - src: carlosbuenosvinos.ansistrano-deploy
    - src: carlosbuenosvinos.ansistrano-rollback
    - src: https://github.com/loric-/ansistrano-package.git

And then install it with.

    $ ansible-galaxy install -p roles -r requirements.yml

## Update

If you want to update the role, you need to pass --force parameter when installing. Please, check the following command.

    $ ansible-galaxy install --force -p roles -r requirements.yml

## Role Variables

    - vars:
      ansistrano_package: "{{ lookup('env','HOME') }}/.ansistrano-package" # Path where the code must be packaged
      
      ansistrano_shared_paths: [] # Shared paths to symlink to release dir
      ansistrano_shared_files: [] # Shared files to symlink to release dir
      ansistrano_unwanted_paths: [] # Unwanted paths
      
      ansistrano_git_repo: git@github.com:USERNAME/REPO.git # Location of the git repository
      ansistrano_git_branch: master # What version of the repository to check out. This can be the full 40-character SHA-1 hash, the literal string HEAD, a branch name, or a tag name
      ansistrano_git_repo_tree: "" # If specified the subtree of the repository to deploy

      ansistrano_env_cleaner_code: "env_code" # env cleaner code
      ansistrano_env_cleaner_wrap_char: "__" # env cleaner character
      ansistrano_env_cleaner_mode: 1 # env cleaner mode
      ansistrano_disable_env_cleaner: no # set yes to disable env cleaner

      ansistrano_changelog_file: changelog.j2 # set the path of changelog template
      ansistrano_disable_changelog: no # set yes to disable changelog

      # Hooks: custom tasks if you need them
      ansistrano_before_setup_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-before-setup-tasks.yml"
      ansistrano_after_setup_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-after-setup-tasks.yml"
      ansistrano_before_git_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-before-git-tasks.yml"
      ansistrano_after_git_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-after-git-tasks.yml"
      ansistrano_before_cleanup_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-before-cleanup-tasks.yml"
      ansistrano_after_cleanup_tasks_file: "{{ playbook_dir }}/<your-deployment-config>/my-after-cleanup-tasks.yml"    

`{{ playbook_dir }}` is an Ansible variable that holds the path to the current playbook.

## Example

You can find an example of use in the example folder.
