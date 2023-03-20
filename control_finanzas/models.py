# Create your models here.

class Expense:
    def __init__(self, value, description, category, photo, id="expense_", user="mock_user"):
        self.id = id
        self.value = value
        self.user = user
        self.description = description
        self.category = category
        self.photo = photo
        
class Goal:
    def __init__(self, enable_target_date, name, set_date, target_date, value, description, category, id="goal_", user="mock_user"):
        self.enable_target_date = enable_target_date
        self.name = name
        self.set_date = set_date
        self.target_date = target_date
        self.value = value
        self.description = description
        self.category = category
        self.id = id
        self.user = user