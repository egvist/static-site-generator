from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html
from split_text import text_to_textnodes


def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)

    html_nodes = []

    for node in text_nodes:
        html_nodes.append(text_node_to_html(node))

    return html_nodes



def heading_to_html(block):
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1:]

    return ParentNode(
        f"h{level}",
        text_to_children(text)
    )


def paragraph_to_html(block):
    text = " ".join(block.split("\n"))

    return ParentNode(
        "p",
        text_to_children(text)
    )


def quote_to_html(block):
    lines = block.split("\n")
    text = " ".join(line[1:].strip() for line in lines)

    return ParentNode(
        "blockquote",
        text_to_children(text)
    )


def code_to_html(block):
    text = block[4:-3]

    if not text.endswith("\n"):
        text += "\n"

    code_node = text_node_to_html(
        TextNode(text, TextType.TEXT)
    )

    return ParentNode(
        "pre",
        [ParentNode("code", [code_node])]
    )


def list_to_html(block, ordered=False):
    lines = block.split("\n")
    items = []

    for line in lines:
        if ordered:
            text = line.split(". ", 1)[1]
        else:
            text = line[2:]

        items.append(
            ParentNode("li", text_to_children(text))
        )

    tag = "ol" if ordered else "ul"
    return ParentNode(tag, items)



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = heading_to_html(block)

        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html(block)

        elif block_type == BlockType.CODE:
            node = code_to_html(block)

        elif block_type == BlockType.QUOTE:
            node = quote_to_html(block)

        elif block_type == BlockType.UNORDERED_LIST:
            node = list_to_html(block)

        elif block_type == BlockType.ORDERED_LIST:
            node = list_to_html(block, ordered=True)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(node)

    return ParentNode("div", children)
