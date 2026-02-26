from Internal.entity.Preset import Preset
from Internal.repository.RepositoryPreset import RepositoryPreset


class PresetService:
    def __init__(self, repository_preset: RepositoryPreset):
        self.__repository = repository_preset

    def create_preset(self, teacher_id, name, data):
        """Creează un obiect Preset și îl trimite către repository."""
        return self.__repository.add_preset(Preset(teacher_id, name, data))

    def get_all_presets_for_teacher(self, teacher_id):
        """Obține lista de preseturi filtrată."""
        return self.__repository.get_presets_by_teacher(teacher_id)

    def delete_preset(self, preset):
        """Șterge un preset prin intermediul repository-ului."""
        return self.__repository.remove_preset(preset)

    def delete_cascade(self, group_id, id_teacher):
        """Șterge grupul din presetări și elimină presetările care rămân goale."""
        presets = self.get_all_presets_for_teacher(id_teacher)

        # Folosim o listă pentru a itera în siguranță dacă decidem să ștergem obiecte
        for preset in presets:
            data = preset.get_data()
            keys_to_remove = [cell_id for cell_id, group_info in data.items()
                              if group_info.get('group_id') == group_id]

            if keys_to_remove:
                for key in keys_to_remove:
                    del data[key]

                # Verificăm dacă preset-ul mai are alte meditații rămase
                if not data:
                    # Dacă e gol, îl ștergem definitiv din repository
                    self.__repository.remove_preset(preset)
                else:
                    # Dacă mai are date, doar îl actualizăm
                    preset.set_data(data)
                    self.__repository.update_preset(preset, preset)

    def set_repository_path(self, path, password):
        self.__repository.set_new_path(path, password)
