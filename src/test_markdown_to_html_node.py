import unittest

from markdown_to_html_node import markdown_to_html_node, extract_title


class Test_Markdown_To_HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_extract_title(self):
        md = """
# This is the title

this is paragraph text

## this is an h2
"""
        actual = extract_title(md)
        expected = "This is the title"
        self.assertEqual(actual, expected)
    
    def test_extract_title_no_title(self):
        md = """
## This is NOT a title

this is paragraph text

## this is an h2
"""
        with self.assertRaises(ValueError):
            extract_title(md)
            self.fail("Exception Expected")
        
    def test_index_file(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """<div><h1>Tolkien Fan Club</h1><p><img src='/images/tolkien.png' alt='JRR Tolkien sitting'></img></p><p>Here's the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote><h2>Blog posts</h2><ul><li><a href='/blog/glorfindel'>Why Glorfindel is More Impressive than Legolas</a></li><li><a href='/blog/tom'>Why Tom Bombadil Was a Mistake</a></li><li><a href='/blog/majesty'>The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here's what <code>elflang</code> looks like (the perfect coding language):</p><pre><code>
func main(){
    fmt.Println("Aiya, Ambar!")
}
</code></pre><p>Want to get in touch? <a href='/contact'>Contact me here</a>.</p><p>This site was generated with a custom-built <a href='https://www.boot.dev/courses/build-static-site-generator-python'>static site generator</a> from the course on <a href='https://www.boot.dev'>Boot.dev</a>.</p></div>"""
        self.maxDiff = None
        self.assertEqual(
            html,
            expected
        )
