from gitlabform.gitlab.core import GitLabCore, NotFoundException


class GitLabGroups(GitLabCore):

    def get_groups(self):
        """
        :return: sorted list of groups
        """
        result = self._make_requests_to_api("groups?all_available=true", paginated=True)
        return sorted(map(lambda x: x['full_path'], result))

    def get_projects(self, group):
        """
        :param group: group name
        :return: sorted list of strings "group/project_name". Note that only projects from "group" namespace are
                 returned, so if "group" (= members of this group) is also a member of some projects, they won't be
                 returned here.
        """
        try:
            projects = self._make_requests_to_api("groups/%s/projects?include_subgroups=true", group, paginated=True)
        except NotFoundException:
            projects = []

        all_project_and_groups = sorted(map(lambda x: x['path_with_namespace'], projects))

        project_and_groups_in_group_namespace = [x for x in all_project_and_groups if x.startswith(group + '/')]

        return project_and_groups_in_group_namespace

    def post_group_secret_variable(self, group, secret_variable):
        # secret_variable has to be like this:
        # {
        #     'key': key,
        #     'value': value,
        #     "variable_type": "env_var",
        #     "protected": false
        # }
        # ..as documented at: https://docs.gitlab.com/ce/api/build_variables.html#create-variable
        self._make_requests_to_api("groups/%s/variables", group, 'POST', secret_variable,
                                   expected_codes=201)

    def put_group_secret_variable(self, group, secret_variable):
        # secret_variable has to be like this:
        # {
        #     'key': key,
        #     'value': value,
        #     "variable_type": "env_var",
        #     "protected": false
        # }
        # ..as documented at: https://docs.gitlab.com/ce/api/build_variables.html#update-variable
        self._make_requests_to_api("groups/%s/variables/%s", (group, secret_variable['key']),
                                   'PUT', secret_variable)

    def get_group_secret_variable(self, group, secret_variable_key):
        return self._make_requests_to_api("groups/%s/variables/%s", (group, secret_variable_key))['value']

    def get_group_secret_variables(self, group):
        return self._make_requests_to_api("groups/%s/variables", group)