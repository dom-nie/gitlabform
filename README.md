[![PyPI version](https://badge.fury.io/py/gitlabform.svg)](https://badge.fury.io/py/gitlabform)
[![Build Status](https://travis-ci.org/egnyte/gitlabform.svg?branch=master)](https://travis-ci.org/egnyte/gitlabform)

# GitLabForm

GitLabForm is an easy configuration as code tool for GitLab using config in plain YAML.

## Features

GitLabForm enables you to manage:

* Project settings,
* Project members (users and groups),
* Deployment keys,
* Secret variables (on project and group/subgroup level),
* Branches (protect/unprotect),
* Tags (protect/unprotect),
* Services,
* (Project) Hooks,
* (Project) Push Rules,
* (Add/edit or delete) Files, with templating based on jinja2 (now supports custom variables!),
* Merge Requests approvals settings and approvers (EE 10.6+ only),

...for:

* all projects you have access to,
* a group/subgroup of projects,
* a single project,

...and a combination of them (default config for all projects + more specific for some groups/subgroups + even more specific for particular projects).

## Installation

1. pip3: `pip3 install gitlabform` - that's all!

2. docker: you can wrap running gitlabform as a docker command, minimal version of it is: `alias gitlabform='docker run -it -v $(pwd):/config egnyte/gitlabform:latest gitlabform`. You can use any version of gitlabform with suffix -alpine3.9 (recommended) or -debian9, depending on your specific needs.

## Quick start

Let's assume that you want to have the same deployment key in all projects in a group "My Group" (with path "my-group").
If so then:

1. Create example `config.yml`:

```yaml
gitlab:
  # You can also set in your environment GITLAB_URL
  url: https://gitlab.yourcompany.com
  # You can also set in your environment GITLAB_TOKEN
  token: "<private token of an admin user>"
  api_version: 4
  ssl_verify: true

group_settings:
  my-group:
    deploy_keys:
      a_friendly_deploy_key_name:
        key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3WiHAsm2UTz2dU1vKFYUGfHI1p5fIv84BbtV/9jAKvZhVHDqMa07PgVtkttjvDC8bA1kezhOBKcO0KNzVoDp0ENq7WLxFyLFMQ9USf8LmOY70uV/l8Gpcn1ZT7zRBdEzUUgF/PjZukqVtuHqf9TCO8Ekvjag9XRfVNadKs25rbL60oqpIpEUqAbmQ4j6GFcfBBBPuVlKfidI6O039dAnDUsmeafwCOhEvQmF+N5Diauw3Mk+9TMKNlOWM+pO2DKxX9LLLWGVA9Dqr6dWY0eHjWKUmk2B1h1HYW+aUyoWX2TGsVX9DlNY7CKiQGsL5MRH9IXKMQ8cfMweKoEcwSSXJ
        title: ssh_key_name_that_is_shown_in_gitlab
        can_push: false
```

2. Run `gitlabform my-group`

3. Watch GitLabForm add this deploy key to all projects in "My Group" group in your GitLab!

## Configuration syntax

See [config.yml](https://github.com/egnyte/gitlabform/blob/master/config.yml) in this repo as a well documented example of configuring all projects in all groups,
projects in "my-group" group and specifically project "my-group/my-project1".

## More usage examples

To apply settings for a single project, run:

```gitlabform my-group/my-project1```

To apply settings for a group of projects, run:

```gitlabform my-group```

To apply settings for all groups of projects and projects explicitly defined in the config, run:

```gitlabform ALL_DEFINED```

To apply settings for all projects, run:

```gitlabform ALL```

If you are satisfied with results consider running it with cron on a regular basis to ensure that your
GitLab configuration stays the way defined in your config (for example in case of some admin changes
some project settings temporarily by (yuck!) clicking).

## All command line parameters

Run:

```gitlabform -h```

...to see the current set of supported command line parameters.

## Requirements

* Python 3.5+
* GitLab 11+ for gitlabform >=1.0.0, GitLab 9.1-10.8 for gitlabform <1.0.0, (GitLab EE 10.6+ for merge_requests section)

## Why?

This tool was created as a workaround for missing GitLab features such as [assigning deploy keys per project groups](https://gitlab.com/gitlab-org/gitlab-ce/issues/3890)
but as of now we prefer to use it ever if there are appropriate web UI features, such as [secret variables per project groups](https://gitlab.com/gitlab-org/gitlab-ce/issues/12729)
(released in GitLab 9.4) to keep configuration as code.

GitLabForm is slightly similar to [GitLab provider](https://www.terraform.io/docs/providers/gitlab/index.html) for Terraform (which we love, btw!),
but it has much more features and uses simpler configuration format.

## How does it work?

It just goes through a loop of projects list and make a series of GitLab API requests. Where possible it corresponds to
GitLab API 1-to-1, so for example it just PUTs or POSTs the hash set at given place in its config transformed into JSON,
so that it's not necessary to modify the app in case of some GitLab API changes.

## Gitlab CI/CD support

You can use gitlabform as a part of your [CCA](https://en.wikipedia.org/wiki/Continuous_configuration_automation) pipeline, example for gitlab could be found at .gitlab-ci.example.yml file. Important note is that when you are exposing your configuration to the pipeline, you have to ensure that token with access to gitlab instance is well protected. Recommended way to do that is to set GITLAB_TOKEN as an environment variable in your pipeline.

## Contributing

Development environment setup how-to:

1. Install build requirements - `pandoc` binary package + `pypandoc` python package.

2. Create virtualenv with Python 3.5+, for example in `venv` dir which is in `.gitignore`.

3. Activate the virtualenv and install gitlabform in it in develop mode (`python setup.py develop`).

## License

MIT
