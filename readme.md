# replace_package_name

start from this repo and do the following steps

- search and replace the string `ReplaceSkillName` everywhere in this repo
- search and replace the string `replace_package_name` everywhere in this repo
- search and replace the string `replace-repo-name` everywhere in this repo
- search and replace the string `replace-author` everywhere in this repo
- create dev and master branches
- make dev default branch
- set PYPI_TOKEN in action secrets
- disable wiki/projects
- disable merge commits and enable auto deletion of head branches on PR merge
- edit license_tests.py settings to your liking
- setup codecov

workflows are setup so you never touch a version file, make a github release or publish to pypi manually again!

- on PR to dev
  - alpha version published and github prerelease created
  - run codecov
  - run unit tests
  - run license tests if requirements.txt changes
  - run build tests
- on commit to master
  - run unit tests
  - run license tests
  - run build tests
- manually trigger one of the workflows for major/minor/build/alpha release in the actions tab
  - increase package version
  - generate changelog
  - commit version bump to dev
  - merge dev to master
  - create github release
  - publish to pypi
- manually trigger a push dev -> master


