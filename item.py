class item:
    """
    constructor for item
    name - name of item - string
    description - description of item - string
    cost - the cost of the item - integer
    health_recovered - the amount of health recovered when the item is used - integer
    is_revive - a boolean stating whether the item is a revive potion or not
    """

    def __init__(self, name, description, cost, health_recovered, is_revive):
        self.name = name
        self.description = description
        self.cost = cost
        self.health_recovered = health_recovered
        self.is_revive = is_revive
    # Getter methods
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

    def get_health_recovered(self):
        return self.health_recovered

    def get_is_revive(self):
        return self.is_revive

    # Setter methods
    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_cost(self, cost):
        self.cost = cost

    def set_health_recovered(self, health_recovered):
        self.health_recovered = health_recovered

    def set_is_revive(self, is_revive):
        self.is_revive = is_revive
