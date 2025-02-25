from unittest import TestCase

from utils import regex

text1 = 'I went to school at https://wwww.homeschool.com/index.html?=school_name and it was amazing.'
text2 = 'We do HTML tags some times in Markup for newline such as <br>new line</br>. Or even <p>test</p>.'
text3 = 'Test driven development (TDD) is encouraged in Agile development.'


class Test(TestCase):
    def test_remove_url(self):
        clean = regex.remove_url(text1)
        self.assertEqual(clean, 'I went to school at  and it was amazing.')

    def test_remove_html(self):
        clean = regex.remove_html(text2)
        self.assertEqual(clean, 'We do HTML tags some times in Markup for newline such as new line. Or even test.')

    def test_remove_bracketed_Text(self):
        clean = regex.remove_bracketed_text(text3)

        # Also remove the extra space.
        clean = regex.remove_extra_space(clean)
        self.assertEqual(clean, 'Test driven development is encouraged in Agile development.')

    def test_transform_contradictions(self):
        clean = regex.transform_contractions("They don't mean but we'd")
        self.assertEqual(clean, "They do not mean but we would")

    def test_get_words(self):
        text = text1 + ' ' + text2 + ' ' + ' ' + text3 + " Also, don't forget date like today 25-03-2025"
        clean = regex.remove_url(text)
        clean = regex.remove_html(clean)
        clean = regex.remove_bracketed_text(clean)
        clean = regex.transform_contractions(clean)
        clean = regex.get_words(clean.lower())
        clean = regex.remove_extra_space(clean)

        # There is trailing empty space (after the last word) - don't delete!
        expected = ("i went to school at and it was amazing we do html tags some times in markup for newline such as "
                    "new line or even test test driven development is encouraged in agile development also do not "
                    "forget date like today ")

        self.assertEqual(clean, expected)
