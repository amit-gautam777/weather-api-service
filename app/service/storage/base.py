from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, object_name: str):
        pass
    
    @abstractmethod
    def get_file(self, object_name: str, download_path: str):
        pass
