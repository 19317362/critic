GIT_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    if to_commit:
        if from_commit:
            what = [from_commit.sha1 + ".." + to_commit.sha1]
        else:
            what = [GIT_EMPTY_TREE, to_commit.sha1]
        what = [commit.sha1]
        what = [commit.parents[0] + '..' + commit.sha1]
        names = repository.run(command, *(options + ["--name-only"] + what))
    options.extend(what)
                if old_mode is not None or new_mode is not None:
        lines = isplitlines(repository.run(command, '--full-index', '--unified=1', *(what + ['--', path])))
    if to_commit:
        elif from_commit:
        else:
            return { None: files }