class item:
    """
    constructor for item
    name - name of item - string
    description - description of item - string
    cost - the cost of the item - integer
    health_recovered - the amount of health recovered when the item is used - integer
    """

    def __init__(self, name, description, cost, health_recovered):
        self.name = name
        self.description = description
        self.cost = cost
        self.health_recovered = health_recovered

    # Getter methods
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

    def get_health_recovered(self):
        return self.health_recovered

    # Setter methods
    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_cost(self, cost):
        self.cost = cost

    def set_health_recovered(self, health_recovered):
        self.health_recovered = health_recovered