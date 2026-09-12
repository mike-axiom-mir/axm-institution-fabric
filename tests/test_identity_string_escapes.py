from __future__ import annotations

import unittest

from axm_institution.identity import canonical_bytes, parse_json_strict


class CanonicalStringEscapeTests(unittest.TestCase):
    def test_adv_023_a_solidus_is_literal_for_values_and_keys(self):
        self.assertEqual(canonical_bytes("a/b"), b'"a/b"')
        self.assertEqual(canonical_bytes({"a/b": "c/d"}), b'{"a/b":"c/d"}')
        self.assertEqual(canonical_bytes(parse_json_strict('"a\\/b"')), b'"a/b"')

    def test_decision_004_quote_reverse_solidus_and_short_controls(self):
        self.assertEqual(canonical_bytes('"'), b'"\\\""')
        self.assertEqual(canonical_bytes("\\"), b'"\\\\"')
        witnesses = {
            "\b": b'"\\b"',
            "\t": b'"\\t"',
            "\n": b'"\\n"',
            "\f": b'"\\f"',
            "\r": b'"\\r"',
        }
        for value, expected in witnesses.items():
            with self.subTest(value=repr(value)):
                self.assertEqual(canonical_bytes(value), expected)

    def test_decision_004_non_short_controls_use_lowercase_hex(self):
        self.assertEqual(canonical_bytes("\x00"), b'"\\u0000"')
        self.assertEqual(canonical_bytes("\x0b"), b'"\\u000b"')
        self.assertEqual(canonical_bytes("\x1f"), b'"\\u001f"')

    def test_decision_004_non_ascii_scalars_are_literal_utf8(self):
        self.assertEqual(canonical_bytes("é"), '"é"'.encode("utf-8"))
        self.assertEqual(canonical_bytes("\u2028"), '"\u2028"'.encode("utf-8"))
        self.assertEqual(canonical_bytes("\u2029"), '"\u2029"'.encode("utf-8"))
        self.assertNotEqual(canonical_bytes("é"), b'"\\u00e9"')


if __name__ == "__main__":
    unittest.main()
