import mesa
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agent import Firefly


class FireFlyWorld(mesa.Model):
    """
    Simple FF world model.
    """

    def __init__(self, width=30, height=300, cycle_len = 10, flash_len = 1, density = .2):
        super().__init__
        """
        Create a new Ff model.
        Args:
            width, height: The size of the grid to model
            cycle_len: the amount of time a ff will wait before flashing again
            flash_len: how long a flash will last for
        """
        # Set up model objects
        self.cycle_len = cycle_len
        self.flash_len = flash_len
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(height, width, torus = True)
        self.do = DataCollector({"Lit": lambda m: self.count_flash()})
        # self.schedule = mesa.time.RandomActivation(self)
        # self.grid = mesa.space.Grid(width, height, torus=False)

        # self.datacollector = mesa.DataCollector(
        #     {
        #         "Lit": lambda m: self.count_type(m, "Lit"),
        #         "Dark": lambda m: self.count_type(m, "Dark")
        #     }
        # )

        for i in range(500):
            pos = ((self.random.randint(0, width - 1)), (self.random.randint(0, height - 1)))
            f = Firefly(self.unique_id, pos, self)
            self.grid.place_agent(f, pos)
            self.schedule.add(f)
        self.running = True


        # for (contents, x, y) in self.grid.coord_iter():
        #     # Create a tree
        #     new_Ff = Firefly((x, y), self)

        #     if self.random.random() < density:
        #         # Set all trees in the first column on fire.
        #         if x == 0:
        #             new_Ff.condition = "Lit"
        #         else:
        #             new_Ff.condition = "Dark"
        #     self.grid.place_agent(new_Ff, (x, y))
        #     self.schedule.add(new_Ff)

        # self.running = True
        # self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        self.datacollector.collect(self)

        if self.schedule.time > 500:
            self.running = False

    def count_flash(self):
        count = 0
        for ff in self.schedule.agents:
            if ff.flash():
                count += 1
        return count
