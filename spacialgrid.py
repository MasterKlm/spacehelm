class SpatialGrid:
    def __init__(self, cellSize):
        self.cellSize = cellSize
        self.grid = {}  # dictionary: (cellX, cellY) -> set of object IDs
        self.entity_registry = {}  # Track what each ID represents: id -> (entity_ref, entity_type)

    def _getCellCoords(self, x, y):
        """Convert world coordinates into grid cell coordinates."""
        return (int(x) // self.cellSize, int(y) // self.cellSize)

    def addClient(self, obj_id, x, y, entity_ref=None, entity_type=None):
        """Add an object (by ID) to the grid based on its position."""
        cell = self._getCellCoords(x, y)
        if cell not in self.grid:
            self.grid[cell] = set()
        self.grid[cell].add(obj_id)
        
        # Track entity for debugging/filtering
        if entity_ref is not None and entity_type is not None:
            self.entity_registry[obj_id] = (entity_ref, entity_type)

    def removeClient(self, obj_id, x, y):
        """Remove an object (by ID) from the grid."""
        cell = self._getCellCoords(x, y)
        if cell in self.grid and obj_id in self.grid[cell]:
            self.grid[cell].remove(obj_id)
            if not self.grid[cell]:  # clean up empty cells
                del self.grid[cell]
        
        # Clean up registry
        if obj_id in self.entity_registry:
            del self.entity_registry[obj_id]

    def getNearbyByType(self, x, y, entity_type):
        """Return nearby objects of specific type"""
        nearby = self.getNearby(x, y)
        filtered = []
        for obj_id in nearby:
            if obj_id in self.entity_registry:
                _, registered_type = self.entity_registry[obj_id]
                if registered_type == entity_type:
                    filtered.append(obj_id)
        return filtered

    def moveClient(self, obj_id, oldX, oldY, newX, newY):
        """Update object position if it moves between cells."""
        oldCell = self._getCellCoords(oldX, oldY)
        newCell = self._getCellCoords(newX, newY)
        if oldCell != newCell:
            # Store the registry info before removing
            entity_info = self.entity_registry.get(obj_id, None)
            
            # Remove from old cell
            if oldCell in self.grid and obj_id in self.grid[oldCell]:
                self.grid[oldCell].remove(obj_id)
                if not self.grid[oldCell]:
                    del self.grid[oldCell]
            
            # Add to new cell
            if newCell not in self.grid:
                self.grid[newCell] = set()
            self.grid[newCell].add(obj_id)
            
            # Restore registry info (don't delete it!)
            if entity_info is not None:
                self.entity_registry[obj_id] = entity_info

    def getNearby(self, x, y):
        """Return all objects in the cell and its 8 neighbors."""
        cellX, cellY = self._getCellCoords(x, y)
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = (cellX + dx, cellY + dy)
                if cell in self.grid:
                    neighbors.extend(self.grid[cell])
        return neighbors