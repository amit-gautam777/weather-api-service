from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    def upload_file_content(self, directory_path: str, file_name: str, content: dict, contentType: str):
        pass
    
    @abstractmethod
    def get_file(self, directory_path: str, file_path: str):
        pass
    
    @abstractmethod
    def delete_file(self, directory_path: str, file_path: str):
        pass
