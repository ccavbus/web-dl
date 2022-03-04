from ghapi.all import GhApi
api = GhApi()

owner = 'ghcdn'
repo = 'video-dl'

runs = api.actions.list_workflow_runs_for_repo(owner, repo)
for run in runs.workflow_runs:
    api.actions.delete_workflow_run(owner, repo, run.id)