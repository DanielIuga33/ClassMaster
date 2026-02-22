import uuid
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

    def set_repository_path(self, path, password):  # Adaugă 'password' aici
        """Actualizează calea și parola pentru repository-ul de presetări."""
        self.__repository.set_new_path(path, password)
