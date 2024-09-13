import pickle

class DataLoader:
    """Handles importing and exporting Graphics using pickle."""

    def export_to_pickle(self, graphic: "Graphic", path: str) -> None:
        """Exports the graphic structure to a pickle file and renumbers ids starting from 1."""
        # First, create a new numbering starting from 1 for all components
        self._renumber_ids(graphic)

        # Save the graphic object to the specified path using pickle
        with open(path, 'wb') as file:
            pickle.dump(graphic, file)

    def import_from_pickle(self, path: str) -> "Graphic":
        """Imports the graphic structure from a pickle file and regenerates ids."""
        with open(path, 'rb') as file:
            graphic = pickle.load(file)

        # After loading, regenerate the ids using _generate_id
        self._regenerate_ids(graphic)

        return graphic

    def _renumber_ids(self, graphic: "Graphic") -> None:
        """Renumbers the ids of all components in the structure, starting from 1."""
        id_counter = 1

        def renumber(graphic):
            nonlocal id_counter
            graphic._id = id_counter  # Assign the new id
            id_counter += 1
            for child in graphic.get_children():
                renumber(child)

        renumber(graphic)

    def _regenerate_ids(self, graphic: "Graphic") -> None:
        """Regenerates the ids for all components in the structure using the _generate_id method."""
        from graphic.abstract.graphic import Graphic

        def regenerate(graphic):
            graphic._id = Graphic._generate_id()  # Regenerate the id
            for child in graphic.get_children():
                regenerate(child)

        regenerate(graphic)

