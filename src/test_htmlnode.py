import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # boot.dev
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    # props to html
    def test_props_to_html(self):
        node = HTMLNode("h1", "Test", None, {"style": "color:red;"})
        self.assertEqual(node.props_to_html(), ' style="color:red;"')

    def test_props_to_html2(self):
        node = HTMLNode(
            "a", "Test", None, {"style": "color:red;", "href": "https://www.boot.dev"}
        )
        self.assertEqual(
            node.props_to_html(), ' style="color:red;" href="https://www.boot.dev"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode("h1", "Test", None, None)
        self.assertEqual(node.props_to_html(), "")

    # repr
    def test_repr(self):
        node = HTMLNode("h1", "Test", None, {"style": "color:red;"})
        self.assertEqual(
            repr(node), "HTMLNode(h1, Test, None, {'style': 'color:red;'})"
        )

    def test_repr_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")


class TestLeafNode(unittest.TestCase):
    # to_html
    def test_value_none(self):
        node = LeafNode("div", None, {"style": "color:red;"})
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_tag_none(self):
        node = LeafNode(None, "Test", {"style": "color:red;"})
        self.assertEqual(node.to_html(), "Test")

    def test_w_attr(self):
        node = LeafNode("p", "Test", {"style": "color:red;"})
        self.assertEqual(node.to_html(), '<p style="color:red;">Test</p>')

    def test_wo_attr(self):
        node = LeafNode("div", "Test", None)
        self.assertEqual(node.to_html(), "<div>Test</div>")

    # repr
    def test_repr(self):
        node = LeafNode("p", "Test", {"style": "color:red;"})
        self.assertEqual(repr(node), "LeafNode(p, Test, {'style': 'color:red;'})")

    def test_repr2(self):
        node = LeafNode("p", "Test", None)
        self.assertEqual(repr(node), "LeafNode(p, Test, None)")

    # boot.dev
    def test_to_html1(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html2(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                    {"style": "color:red;"},
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><div style="color:red;"><i>italic text</i>Normal text</div><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )

    # boot.dev
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
