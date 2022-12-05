import mesa


# Step 1 Agent:

class Firefly(mesa.Agent):
    """
    A Firefly. (NOT A LIGHTNING BUG)

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Lit", or "Dark"
        unique_id: (x,y) tuple.
    """

    def __init__(self, unique_id, pos, model):
        """
        Create a new Ff.
        Args:
            pos: The Ff's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(unique_id, pos, model)
        self.pos = pos
        self.clock = self.randomint(1, self.model.cycle_len)

    def flash(self):
        return self.clock <= self.model.flash_len

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        self._next = self.clock + 1
        if self._next > self.model.cycle_len:
            self._next = 1
        
        if not self.flash():
            neighbors = self.model.grid.get_neighbors(self.pos, True)
            for neighbor in neighbors:
                if neighbor.flash():
                    self._next = self.model.flash_len

    def advance(self):
        self.clock = self._next
        self.move()

    def move(self):
        next_m = self.model.grid.get_neighboorhood(self.pos, True, True)
        self._next = self.random_choice(next_m)
        self.model.grid.move_agent(self, next_m)