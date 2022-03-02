# skill-template-repo 

start from this repo and do the following steps

- search and replace the string `ReplaceSkillName` everywhere in this repo
- search and replace the string `skill_template_repo` everywhere in this repo
- search and replace the string `skill-template-repo` everywhere in this repo
- search and replace the string `OpenVoiceOS` everywhere in this repo
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
  - run plugin tests
- on commit to dev
  - auto translate resource files
- manually trigger one of the workflows for major/minor/build/alpha release in the actions tab
  - increase package version
  - generate changelog
  - commit version bump to dev
  - merge dev to master
  - create github release
  - publish to pypi


