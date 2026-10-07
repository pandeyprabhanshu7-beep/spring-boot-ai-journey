import unittest
from teamcity_messages import escape, message


class TeamCityTests(unittest.TestCase):
    def test_all_control_characters(self):
        self.assertEqual(escape("|'\n\r[]"), "|||\'|n|r|[|]")

    def test_plain_text(self):
        self.assertEqual(escape("tenant.alpha"), "tenant.alpha")

    def test_frame(self):
        self.assertEqual(message("testStarted", name="a'b"),
                         "##teamcity[testStarted name='a|'b']")

    def test_reject_control_in_kind(self):
        with self.assertRaises(ValueError):
            message("x]", name="a")


if __name__ == "__main__":
    unittest.main()
