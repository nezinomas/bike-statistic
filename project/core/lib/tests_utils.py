def clean_content(content):
    content = content.decode("utf-8")
    content = content.replace("\n", "")
    content = content.replace("\t", "")
    while "  " in content:
        content = content.replace("  ", " ")

    return content
