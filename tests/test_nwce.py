import unittest
from nwce import CfgBlock


class TestCfgBlock(unittest.TestCase):
    def test_clean_comments(self):
        lines = ["", "!", "! ", "!  ", "line"]
        expected_result = ["", "line"]
        actual_result = CfgBlock._clean_comments(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_clean_comments2(self):
        lines = ["", "#", "! ", "#!  ", "no line"]
        expected_result = ["", "no line"]
        actual_result = CfgBlock._clean_comments(lines, comments="!#")
        self.assertListEqual(actual_result, expected_result)

    def test_clean_comments3(self):
        lines = ["", "$", "$ ", "$  ", "line"]
        expected_result = ["", "line"]
        actual_result = CfgBlock._clean_comments(lines, comments="$")
        self.assertListEqual(actual_result, expected_result)

    def test_clean_blank_lines(self):
        lines = ["", " ", "  ", "\t  ", "no line"]
        expected_result = ["no line"]
        actual_result = CfgBlock._clean_blank_lines(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_indent1(self):
        lines = ["line1", "line2", "  no sub-line"]
        expected_result = ["  line1", "  line2", "    no sub-line"]
        actual_result = CfgBlock.indent(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_indent2(self):
        lines = ["line1", "line2", "  no sub-line"]
        expected_result = lines
        actual_result = CfgBlock.indent(lines, num=0)
        self.assertListEqual(actual_result, expected_result)

    def test_indent3(self):
        lines = ["line1", "line2", "  no sub-line"]
        expected_result = ["    line1", "    line2", "      no sub-line"]
        actual_result = CfgBlock.indent(lines, num=2)
        self.assertListEqual(actual_result, expected_result)

    def test_indent4(self):
        lines = ["line1", "line2", "  no sub-line"]
        expected_result = [" line1", " line2", "   no sub-line"]
        actual_result = CfgBlock.indent(lines, indent=" ")
        self.assertListEqual(actual_result, expected_result)

    def test_indent5(self):
        lines = ["  line1", "  line2", "    no sub-line"]
        expected_result = ["line1", "line2", "  no sub-line"]
        actual_result = CfgBlock.indent(lines, indent="  ", num=-1)
        self.assertListEqual(actual_result, expected_result)

    def test_indent6(self):
        lines = ["  line1", "  line2", "    no sub-line"]
        expected_result = ["line1", "line2", "  no sub-line"]
        actual_result = CfgBlock.indent(lines, indent=" ", num=-2)
        self.assertListEqual(actual_result, expected_result)

    def test_indent7(self):
        lines = ["  line1", "  line2", "    no sub-line"]
        with self.assertRaises(Exception) as context:
            CfgBlock.indent(lines, indent=" ", num=-3)
        self.assertTrue("Line #1: Configuration is not correctly indented!" in context.exception.args)

    def test_parse_blocks1(self):
        lines = []
        expected_result = []
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_blocks2(self):
        lines = ["a", "no b"]
        expected_result = [["a"], ["no b"]]
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_blocks3(self):
        lines = ["a", "  1a", "    no 2a"]
        expected_result = [["a", "  1a", "    no 2a"]]
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_blocks4(self):
        lines = ["a", "  1a", "    no 2a", "b", "  1b", "no c"]
        expected_result = [["a", "  1a", "    no 2a"], ["b", "  1b"], ["no c"]]
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_blocks5(self):
        lines = ["  a", "  no b"]
        expected_result = [["a"], ["no b"]]
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_blocks6(self):
        lines = ["  a", "    no b"]
        expected_result = [["a", "  no b"]]
        actual_result = CfgBlock._parse_blocks(lines)
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block1(self):
        lines = ["a"]
        expected_result = ["a", False, []]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block2(self):
        lines = ["  a"]
        expected_result = ["a", False, []]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block3(self):
        lines = ["    a"]
        expected_result = ["a", False, []]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block4(self):
        lines = ["a", "  a"]
        expected_result = ["a", False, ["a"]]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block5(self):
        lines = ["a", "    a"]
        expected_result = ["a", False, ["a"]]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block6(self):
        lines = ["a", "  a", "  a"]
        expected_result = ["a", False, ["a", "a"]]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse_block7(self):
        lines = ["a", "  a", "    a"]
        expected_result = ["a", False, ["a", "  a"]]
        c = CfgBlock()
        actual_result = list(c._parse_block(lines))
        self.assertListEqual(actual_result, expected_result)

    def test_parse1(self):
        c = CfgBlock()
        self.assertIsNone(c.line)
        self.assertListEqual(c.children, [])

    def test_parse2(self):
        lines = []
        c = CfgBlock(lines)
        self.assertIsNone(c.line)
        self.assertListEqual(c.children, [])

    def test_parse3(self):
        lines = ["a"]
        c = CfgBlock(lines)
        self.assertEqual(c.line, "a")
        self.assertListEqual(c.children, [])

    def test_parse4(self):
        lines = ["a", "b"]
        c = CfgBlock(lines)
        self.assertIsNone(c.line)
        self.assertEqual(len(c.children), 2)
        child1 = c.children[0]
        self.assertEqual(child1.line, "a")
        self.assertListEqual(child1.children, [])
        child2 = c.children[1]
        self.assertEqual(child2.line, "b")
        self.assertListEqual(child2.children, [])

    def test_parse5(self):
        lines = ["a", "  1a", "    2a"]
        c = CfgBlock(lines)
        self.assertEqual(c.line, "a")
        self.assertEqual(len(c.children), 1)
        child = c.children[0]
        self.assertEqual(child.line, "1a")
        self.assertEqual(len(child.children), 1)
        subchild = child.children[0]
        self.assertEqual(subchild.line, "2a")
        self.assertEqual(len(subchild.children), 0)

    def test_parse6(self):
        lines = ["a", "  1a", "    2a", "b", "  1b", "c"]
        c = CfgBlock(lines)
        self.assertIsNone(c.line)
        self.assertEqual(len(c.children), 3)
        childa = c.children[0]
        self.assertEqual(childa.line, "a")
        self.assertEqual(len(childa.children), 1)
        subchilda = childa.children[0]
        self.assertEqual(subchilda.line, "1a")
        self.assertEqual(len(subchilda.children), 1)
        subsubchilda = subchilda.children[0]
        self.assertEqual(subsubchilda.line, "2a")
        self.assertEqual(len(subsubchilda.children), 0)
        childb = c.children[1]
        self.assertEqual(childb.line, "b")
        self.assertEqual(len(childb.children), 1)
        subchildb = childb.children[0]
        self.assertEqual(subchildb.line, "1b")
        self.assertEqual(len(subchildb.children), 0)
        childc = c.children[2]
        self.assertEqual(childc.line, "c")
        self.assertEqual(len(childc.children), 0)

    def test_parse7(self):
        lines = ["no a"]
        c = CfgBlock(lines)
        self.assertEqual(c.line, "a")
        self.assertEqual(c.negate, True)
        self.assertListEqual(c.children, [])

    def test_parse8(self):
        lines = ["a", "no b"]
        c = CfgBlock(lines)
        self.assertIsNone(c.line)
        self.assertIsNone(c.negate)
        self.assertEqual(len(c.children), 2)
        child1 = c.children[0]
        self.assertEqual(child1.line, "a")
        self.assertEqual(child1.negate, False)
        self.assertListEqual(child1.children, [])
        child2 = c.children[1]
        self.assertEqual(child2.line, "b")
        self.assertEqual(child2.negate, True)
        self.assertListEqual(child2.children, [])

    def test_parse9(self):
        lines = ["a", "  no b"]
        c = CfgBlock(lines)
        self.assertEqual(c.line, "a")
        self.assertEqual(c.negate, False)
        self.assertEqual(len(c.children), 1)
        child = c.children[0]
        self.assertEqual(child.line, "b")
        self.assertEqual(child.negate, True)
        self.assertListEqual(child.children, [])

    def test_merge_duplicate_siblings1(self):
        lines = ["1", " a", "1"]
        c = CfgBlock(lines)
        expected_result = ["1", "  a"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings2(self):
        lines = ["1", " a", "1", "  no b"]
        c = CfgBlock(lines)
        expected_result = ["1", "  a", "  no b"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings3(self):
        lines = ["1", " a", "1", "  a"]
        c = CfgBlock(lines)
        expected_result = ["1", "  a"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings4(self):
        lines = ["1", " a", "  no b", "1", "  a", "  c"]
        c = CfgBlock(lines)
        expected_result = ["1", "  a", "    no b", "  c"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings5(self):
        lines = ["1", " a", "  b", "1", "  b", "    no c"]
        c = CfgBlock(lines)
        expected_result = ["1", "  a", "    b", "  b", "    no c"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings6(self):
        lines = ["a", "  b", "no a"]
        c = CfgBlock(lines)
        expected_result = ["no a"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings7(self):
        lines = ["no a", "a", "  c"]
        c = CfgBlock(lines)
        expected_result = ["a", "  c"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge_duplicate_siblings7(self):
        lines = ["no a", "a", "  b", "no a"]
        c = CfgBlock(lines)
        expected_result = ["no a"]
        actual_result = c._merge_duplicate_siblings().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_lines(self):
        lines = ["1", "2", "no 3"]
        c = CfgBlock(lines)
        expected_result = lines.copy()
        actual_result = c.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_lines2(self):
        lines = ["1", "  2", "    no 3"]
        c = CfgBlock(lines)
        expected_result = lines.copy()
        actual_result = c.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_text(self):
        lines = ["1", "2", "no 3"]
        c = CfgBlock(lines)
        expected_result = "1\n2\nno 3"
        actual_result = c.text()
        self.assertEqual(actual_result, expected_result)

    def test_text2(self):
        lines = ["1", " 2", "  no 3"]
        c = CfgBlock(lines)
        expected_result = "1\n  2\n    no 3"
        actual_result = c.text()
        self.assertEqual(actual_result, expected_result)

    def test_sort(self):
        lines = ["a 3", "a 2", "a 1"]
        rules = []
        c = CfgBlock(lines)
        expected_result = list(reversed(lines))
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort2(self):
        lines = ["a 1", "a 2", "a 3"]
        rules = list(reversed(lines))
        c = CfgBlock(lines)
        expected_result = rules
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort3(self):
        lines = ["a 2", "  3", "    2", "    1", "  2", "  1", "a 1", "  no 3", "  2", "  1"]
        rules = []
        c = CfgBlock(lines)
        expected_result = ["a 1", "  1", "  2", "  no 3", "a 2", "  1", "  2", "  3", "    1", "    2"]
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort4(self):
        lines = ["b", "  no b2", "  b1", "a", "  no a2", "  a1"]
        rules = ["a", "  a2", "  a1", "b"]
        c = CfgBlock(lines)
        expected_result = ["a", "  no a2", "  a1", "b", "  b1", "  no b2"]
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort5(self):
        lines = ["b", "a 3 22 1 c"]
        rules = [r"a (?P<params>(?:\d+ ?)+) c", "b"]
        c = CfgBlock(lines)
        expected_result = ["a 1 3 22 c", "b"]
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort6(self):
        lines = ["b", "a a 20", "  x", "a b 10", "  x"]
        rules = [r"a .* (?P<id1>\d+)$", "b"]
        c = CfgBlock(lines)
        expected_result = ["a b 10", "  x", "a a 20", "  x", "b"]
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_sort7(self):
        lines = ["b", "a Z X 20", "  x", "a Z Y 10", "  x", "a A Y 10", "  x", "a A X 20", "  x"]
        rules = [r"a (?P<id1>\w+) .* (?P<id2>\d+)$", "b"]
        c = CfgBlock(lines)
        expected_result = ["a A Y 10", "  x", "a A X 20", "  x", "a Z Y 10", "  x", "a Z X 20", "  x", "b"]
        actual_result = c.sort(rules=CfgBlock(rules)).lines()
        self.assertListEqual(actual_result, expected_result)

    def test_comment(self):
        lines = ["a 1", "a 2", "b", "  no c"]
        c = CfgBlock(lines)
        expected_result = ["a 1", "a 2", "!", "b", "  no c", "!"]
        actual_result = c.lines(comment_line=True)
        self.assertListEqual(actual_result, expected_result)

    def test_comment2(self):
        lines = ["a 1", "no a 2", "b", "  c"]
        c = CfgBlock(lines)
        c.config["comments"] = ""
        expected_result = ["a 1", "no a 2", "", "b", "  c", ""]
        actual_result = c.lines(comment_line=True)
        self.assertListEqual(actual_result, expected_result)

    def test_copy1(self):
        a = CfgBlock(["a"])
        b = a.copy()

        self.assertEqual(a.line, b.line)
        self.assertEqual(len(a.children), 0)
        self.assertEqual(len(b.children), 0)

    def test_merge(self):
        a = CfgBlock(["a"])
        b = CfgBlock(["no b"])
        merge = a + b
        expected_result = ["a", "no b"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge2(self):
        a = CfgBlock(["a"])
        b = CfgBlock(["no b", "c"])
        merge = a + b
        expected_result = ["a", "no b", "c"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge3(self):
        a = CfgBlock(["a", "b"])
        b = CfgBlock(["no c"])
        merge = a + b
        expected_result = ["a", "b", "no c"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge4(self):
        a = CfgBlock(["a", "no b"])
        b = CfgBlock(["c", "no d"])
        merge = a + b
        expected_result = ["a", "no b", "c", "no d"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge5(self):
        a = CfgBlock(["a", "  no 1"])
        b = CfgBlock(["b", "  no 1"])
        merge = a + b
        expected_result = ["a", "  no 1", "b", "  no 1"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge6(self):
        a = CfgBlock(["a", "  no 1"])
        b = CfgBlock(["a", "  2"])
        merge = a + b
        expected_result = ["a", "  no 1", "  2"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge7(self):
        a = CfgBlock(["a", "  b", "    no 1"])
        b = CfgBlock(["a", "  b", "    2"])
        merge = a + b
        expected_result = ["a", "  b", "    no 1", "    2"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge8(self):
        a = CfgBlock(["a", "  b", "    1"])
        b = CfgBlock(["b", "  b", "    no 2"])
        merge = a + b
        expected_result = ["a", "  b", "    1", "b", "  b", "    no 2"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge9(self):
        a = CfgBlock(["a"])
        b = CfgBlock(["no a"])
        merge = a + b
        expected_result = ["no a"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge10(self):
        a = CfgBlock(["no a"])
        b = CfgBlock(["a"])
        merge = a + b
        expected_result = ["a"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge11(self):
        a = CfgBlock(["a", "  b"])
        b = CfgBlock(["no a", "  c"])
        merge = a + b
        expected_result = ["no a", "  c"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_merge12(self):
        a = CfgBlock(["no a", "  b"])
        b = CfgBlock(["a", "  c"])
        merge = a + b
        expected_result = ["a", "  c"]
        actual_result = merge.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff1(self):
        a = CfgBlock(["a"])
        b = CfgBlock(["no b"])
        diff = b - a
        expected_result = ["no a", "no b"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff2(self):
        a = CfgBlock(["a"])
        b = CfgBlock(["a"])
        diff = b - a
        expected_result = []
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff3(self):
        a = CfgBlock(["no a", "b", "no d"])
        b = CfgBlock(["a", "c", "no d"])
        diff = b - a
        expected_result = ["no b", "a", "c"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff4(self):
        a = CfgBlock(["a", "  b", "  no d"])
        b = CfgBlock(["a", "  c"])
        diff = b - a
        expected_result = ["a", "  d", "  no b", "  c"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff5(self):
        a = CfgBlock(["a", "  b", "  no d"])
        b = CfgBlock(["b", "  c", "  no d"])
        diff = b - a
        expected_result = ["no a", "b", "  c", "  no d"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff6(self):
        a = CfgBlock(["a", "  c", "  d", "no b"])
        b = CfgBlock(["a", "b", "  c", "  d"])
        diff = b - a
        expected_result = ["b", "  c", "  d", "a", "  no d", "  no c"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_diff7(self):
        a = CfgBlock(["a 20", "  b", "  c"])

        b = CfgBlock(["no a 20", "a 10", "  c"])

        diff = b - a
        expected_result = ["no a 20", "a 10", "  c"]
        actual_result = diff.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter0(self):
        a = CfgBlock(["a", "b", "  c"])

        res = a.filter("")
        expected_result = ["a", "b", "  c"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter1(self):
        a = CfgBlock(["a"])

        res = a.filter("a")
        expected_result = ["a"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("b")
        expected_result = []
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter2(self):
        a = CfgBlock(["a", "b"])

        res = a.filter("a")
        expected_result = ["a"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("b")
        expected_result = ["b"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter3(self):
        a = CfgBlock(["a", "  b"])

        res = a.filter("a")
        expected_result = ["a", "  b"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("b")
        expected_result = ["a", "  b"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter4(self):
        a = CfgBlock(["a", "  b", "  c"])

        res = a.filter("a")
        expected_result = ["a", "  b", "  c"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("b")
        expected_result = ["a", "  b"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_filter5(self):
        a = CfgBlock(["a", "  a", "    b", "    c", "    d"])

        res = a.filter("a")
        expected_result = ["a", "  a", "    b", "    c", "    d"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("b")
        expected_result = ["a", "  a", "    b"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("c")
        expected_result = ["a", "  a", "    c"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

        res = a.filter("d")
        expected_result = ["a", "  a", "    d"]
        actual_result = res.lines()
        self.assertListEqual(actual_result, expected_result)

    def test_negative_first1(self):
        cfg = CfgBlock(["a", "no b", "c", "no d"])

        expected_result = ["no d", "no b", "a", "c"]
        actual_result = cfg.negative_first().lines()
        self.assertListEqual(actual_result, expected_result)

    def test_negative_first2(self):
        cfg = CfgBlock(["a", "  no b", "  c", "  no d"])

        expected_result = ["a", "  no d", "  no b", "  c"]
        actual_result = cfg.negative_first().lines()
        self.assertListEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
