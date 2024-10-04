import pickle

class DataLoader:
    """Handles importing and exporting Graphics using pickle."""
    
    def export_to_pickle(self, component: 'Graphic', path: str) -> None:
        """Exports the component structure to a pickle file and renumbers ids starting from 1."""
        # First, create a new numbering starting from 1 for all components
        self._renumber_ids(component)
        
        # Save the component object to the specified path using pickle
        with open(path, 'wb') as file:
            pickle.dump(component, file)

    def import_from_pickle(self, path: str) -> 'Graphic':
        """Imports the component structure from a pickle file and regenerates ids."""
        with open(path, 'rb') as file:
            component = pickle.load(file)
        
        # After loading, regenerate the ids using _generate_id
        self._regenerate_ids(component)
        
        return component
    
    def _renumber_ids(self, component: 'Graphic') -> None:
        """Renumbers the ids of all components in the structure, starting from 1."""
        id_counter = 1

        def renumber(comp):
            nonlocal id_counter
            comp._id = id_counter  # Assign the new id
            id_counter += 1
            for child in comp.get_children():
                renumber(child)

        renumber(component)

    def _regenerate_ids(self, component: 'Graphic') -> None:
        from .graphic.abstract.graphic import Graphic
        """Regenerates the ids for all components in the structure using the _generate_id method."""
        def regenerate(comp):
            comp._id = Graphic._generate_id()  # Regenerate the id
            for child in comp.get_children():
                regenerate(child)

        regenerate(component)