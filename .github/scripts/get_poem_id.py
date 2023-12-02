#!/usr/bin/env python

import sys
import subprocess
import json

NOT_FOUND = 0
ERROR = -1


def get_poem_id(repository, pull_id):
    """
    Read the body of a pull request from stdin, write ID of any associated POEM to stdout.

    Parameters
    ----------
    repository : str
        The owner and repository name. For example, 'octocat/Hello-World'.
    pull_id : str
        The id of a pull request.

    Returns
    -------
    int
        The ID of the associated POEM, or 0 if an associated POEM ID was found
    """
    print("-------------------------------------------------------------------------------")
    print(f"Checking Pull Request #{pull_id} for associated issue...")
    print("-------------------------------------------------------------------------------")
    try:
        pull_json = subprocess.check_output(["gh", "--repo", repository,
                                            "issue", "view", "--json", "body", pull_id])
    except subprocess.CalledProcessError as err:
        print(f"Unable to access pull request #{pull_id}:\nrc={err.returncode}")
        return ERROR

    pull_body = json.loads(pull_json)["body"]

    issue_id = ""

    for line in pull_body.splitlines():
        print(line)
        if "Resolves #" in line:
            issue_id = line[line.index("Resolves #") + 10:].strip()
            break

    print("----------------")
    print(f"{issue_id=}")
    print("----------------")

    if not issue_id.isnumeric():
        # issue ID not found, could be blank or "N/A"
        return NOT_FOUND

    print("-------------------------------------------------------------------------------")
    print(f"Checking Issue #{issue_id} for associated POEM...")
    print("-------------------------------------------------------------------------------")

    # for debugging only
    # repository = 'OpenMDAO/OpenMDAO'

    try:
        issue_json = subprocess.check_output(["gh", "--repo", repository,
                                            "issue", "view", "--json", "body", issue_id])
    except subprocess.CalledProcessError as err:
        print(f"Unable to access issue  #{issue_id}:\nrc={err.returncode}")
        return ERROR

    issue_body = json.loads(issue_json)["body"]

    poem_id = ""

    associated_poem = False

    for line in issue_body.splitlines():
        print(line)
        # POEM ID is found on the line following the "Associated POEM" label
        if "Associated POEM" in line:
            associated_poem = True
        elif associated_poem:
            poem_id = line.strip()
            if poem_id:
                break

    print("----------------")
    print(f"{poem_id=}")
    print("----------------")

    if 'POEM_' in poem_id:
        poem_id = poem_id[5:]
    elif 'POEM' in poem_id:
        poem_id = poem_id[4:]

    if not poem_id.isnumeric():
        # poem ID not found, could be blank or "_No response_"
        return NOT_FOUND
    else:
        return int(poem_id)


if __name__ == '__main__':
    exit(get_poem_id(sys.argv[1], sys.argv[2]))
