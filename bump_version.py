from enum import Enum
from functools import lru_cache
from git import Repo, TagReference, Commit
import subprocess
import sys
from typing import Iterable, Tuple


LOGGING = True


def log(*args, **kwargs):
    if LOGGING:
        print(*args, **kwargs)


class VersionIncrement(Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    PATCH = 'patch'
    DEVELOPMENT = 'dev'


def version_increment(majors: int, minors: int, patches: int, dev: int) -> VersionIncrement:
    if majors:
        return VersionIncrement.MAJOR
    if minors:
        return VersionIncrement.MINOR
    if patches:
        return VersionIncrement.PATCH
    return VersionIncrement.DEVELOPMENT


def find_last_tag(repo: Repo) -> TagReference:
    last_tag_name = repo.git.describe('--tags', '--abbrev=0')
    return repo.tags[last_tag_name]


def all_commits_up_to_tag(repo: Repo, tag: TagReference = None) -> Iterable[Commit]:
    tag = tag or find_last_tag(repo)
    for commit in repo.iter_commits():
        if commit == tag.commit:
            break
        yield commit


def comput_version_increment_from(commits: Iterable[Commit]) -> Tuple[VersionIncrement, int]:
    major_changes, minor_changes, patch_changes, dev_changes = 0, 0, 0, 0
    for index, commit in enumerate(commits):
        log(f"{index + 1}. {commit.hexsha}: `{commit.summary.strip()}`")
        if 'BREAKING CHANGE:' in commit.message:
            major_changes += 1
            log(f"   + **major** change: `BREAKING CHANGE:` found in summary")
        if ':' not in commit.summary:
            log(f"   + considered as **dev** change: commit message is not conventional")
            major_changes += 1
        description = commit.summary.split(':')[0]
        if description.endswith('!'):
            major_changes += 1
            log(f"   + **major** change: `!` found in description")
        if description.startswith('feat'):
            minor_changes += 1
            log(f"   + **minor** change: `feat` found in description")
        if description.startswith('fix'):
            patch_changes += 1
            log(f"   + **patch** change: `fix` found in description")
        dev_changes += 1
        log(f"   + **dev** change: commit is described as `{description}`")
    increment = version_increment(major_changes, minor_changes, patch_changes, dev_changes)
    log(f"\nTotal commits: {dev_changes}, of which:")
    log(f"- {major_changes} major changes")
    log(f"- {minor_changes} minor changes")
    log(f"- {patch_changes} patch changes\n")
    return increment, dev_changes


def _poetry(*args):
    return subprocess.run([sys.executable, "-m", "poetry", *args], capture_output=True, text=True).stdout.strip()


@lru_cache
def get_current_version() -> str:
    return _poetry("version", "--short")


def update_version(increment: VersionIncrement, n_changes: int, apply: bool = False):
    target = f"{get_current_version()}-dev{n_changes}" \
        if increment == VersionIncrement.DEVELOPMENT \
        else increment.value
    args = ["version", "--short", target] + ([] if apply else ['--dry-run'])
    version = _poetry(*args)
    log("hence, next version is: `", end='')
    print(version + ('`' if LOGGING else ''))
    get_current_version.cache_clear()
            

if __name__ == '__main__':
    with Repo('.') as repo:
        LOGGING = "--silent" not in sys.argv
        last_tag = find_last_tag(repo)
        current_version = get_current_version()
        log(f"From commit {last_tag.commit.hexsha} (corresponding to v`{current_version}`):")
        commits = all_commits_up_to_tag(repo, )
        version, n_changes = comput_version_increment_from(commits)
        actually_apply = "--apply" in sys.argv
        update_version(version, n_changes, actually_apply)
