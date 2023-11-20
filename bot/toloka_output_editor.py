class TolokaEditor:
    def __init__(self):
        with open('./categories.txt', 'r', encoding='utf-8') as categories:
            self.categories = [category.strip() for category in categories.readlines()]

    def check_categories_in_result(self, generated_result):
        if generated_result:
            if generated_result['selected_field'] not in self.categories:
                generated_result['selected_field'] = 'Another'
            if generated_result['Garbage'] == 'True':
                generated_result['selected_field'] = self.categories[0]
        return generated_result
