class Note:
    def __init__(self, id, name_category, title, text, photo):
        self.id = id
        self.name_category = name_category
        self.title = title
        self.text = text
        self.photo = photo

    def __str__(self):
        return f'{self.name_category}\n{self.title}\n{self.text}'

