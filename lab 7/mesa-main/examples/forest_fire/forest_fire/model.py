import mesa

from .agent import TreeCell


class ForestFire(mesa.Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65):

        super().__init__(*args, **kwargs)
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        


        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.Grid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Empty": lambda m: self.count_type(m, "Empty")
            }
        )

    # def setup_grid(self, density: float):
        # for (contents, x, y) in self.grid.coord_iter():
            # new_tree = Tree(self, (x, y) self.random.uniform(0, self.lifetime))

            # if self.random.random() < density: 
            # new_tree.grow()  


        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            # Create a tree
            new_tree = TreeCell((x, y), self)

            if self.random.random() < density:
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                else:
                    new_tree.condition = "Fine"
            self.grid.place_agent(new_tree, (x, y))
            self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

        # if self.get_condition() == "On Fire":
        # if self.get_condition() == "Empty":
        # if self.get_condition() == "Fine":


    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

    def decay(self):
        self.condition = "Empty"
        self.decay_time = 0

    def ignite(self):
        self.condition = "On Fire"

    def burn_out(self):
        self.condition = "Burned Out"



# diffusion notes
# self._nextAmount = (1 - self.model.evaporate) * (self.amount + (self.model.diffusion * (ave_p - self.amount)))

# if self._nextAmoun < self.model.lowerbound:
#   self._nextAmount = 0

# Wind strength = 0.1

# for n in neighbors:
    #nx, ny = n.pos
    # x, y = self.pos

    # if nx > x and y == ny:
        # due_to_wind = wind_strength * self._netAmount
        # self._nextAmount -= due_to_wind
        # n.add(due_to_wind)

# def advance(self):
#    self.amount = self._nextAmount