from ovos_skills_manager import SkillEntry
# write your first unittest!
import unittest
from ovos_plugin_manager.skills import find_skill_plugins
from os.path import exists
from shutil import rmtree

branch = "dev"
url = f"https://github.com/replace-author/replace-repo-name@{branch}"
# TODO delete this override when making a new skill
url = f"https://github.com/OpenVoiceOS/skill-template-repo@{branch}"


class TestOSM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.skill_id = "replace-repo-name.replace-author"

    def test_osm_install(self):
        skill = SkillEntry.from_github_url(url)
        tmp_skills = "/tmp/osm_installed_skills"
        skill_folder = f"{tmp_skills}/{skill.uuid}"

        if exists(skill_folder):
            rmtree(skill_folder)

        updated = skill.install(folder=tmp_skills, default_branch=branch)
        self.assertEqual(updated, True)
        self.assertTrue(exists(skill_folder))

        updated = skill.install(folder=tmp_skills, default_branch=branch)
        self.assertEqual(updated, False)




