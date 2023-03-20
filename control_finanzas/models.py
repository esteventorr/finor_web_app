# Create your models here.

class Expense:
    def __init__(self, value, description, category, photo, id="expense_", user="mock_user"):
        self.id = id
        self.value = value
        self.user = user
        self.description = description
        self.category = category
        self.photo = photo