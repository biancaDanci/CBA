def validate_boilerpipe():
    import requests
    import justext

    response = requests.get("http://www.cs.ubbcluj.ro/en/")
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            print(paragraph.text)
    import pdb
    pdb.set_trace()

validate_boilerpipe()
