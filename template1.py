from abc import ABC, abstractmethod
from typing import List, Dict
import json
import csv

class DataLoader(ABC):
    content: List[Dict] = []
    filename: str = ''
    
    def template_method(self) -> None:
        self.load_content()
        self.save_content()
        self.display_content()
        
    def display_content(self) -> None:
        for c in self.content:
            print(c)
     
    @abstractmethod       
    def load_content(self) -> bool:
        pass
    
    @abstractmethod
    def save_content(self, file: str) -> None:
        pass
    
class CSVDataLoader(DataLoader):
    def __init__(self, filename) -> None:
        self.filename: str = filename
        
    def load_content(self) -> bool:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.content = list(csv.DictReader(f))
            return True
        
        except Exception as e:
            print(f'Error loading CSV data: {e}')
            return False;
    
    def save_content(self, file: str) -> None:
        try:
            with open(file, 'w', encoding='utf-8') as f:
                csv_writer = csv.DictWriter(f, fieldnames=self.content[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(self.content)
        
        except Exception as e:
            print(f'Error saving CSV data: {e}')
    
class JSONDataLoader(DataLoader):
    def __init__(self, filename) -> None:
        self.filename: str = filename
        
    def load_content(self) -> bool:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.content = json.load(f)
            return True
        
        except Exception as e:
            print(f'Error loading JSON data: {e}')
            return False;
    
    def save_content(self, file: str) -> None:
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self.content, f, indent=2)
        
        except Exception as e:
            print(f'Error saving JSON data: {e}')
            
if __name__ == '__main__':
    csv_data_loader: DataLoader = CSVDataLoader('template1.csv')
    json_data_loader: DataLoader = JSONDataLoader('template1.json')
    
    example_new: Dict = {'name': 'Gregory', 'age': 45, 'hobby': 'Swimming'}
    
    csv_data_loader.load_content()
    json_data_loader.load_content()
    
    print('CSV results: ')
    csv_data_loader.display_content()
    
    print('JSON results: ')
    json_data_loader.display_content()
    print()
    
    print('Saving tests: ')
    csv_data_loader.content.append(example_new)
    csv_data_loader.save_content('tmp.csv')
    
    json_data_loader.content.append(example_new)
    json_data_loader.save_content('tmp.json')
    print('Saved\n')
    
    csv_data_loader.filename = 'tmp.csv'
    json_data_loader.filename = 'tmp.json'
    
    print('CSV new results: ')
    csv_data_loader.display_content()
    
    print('JSON new results: ')
    json_data_loader.display_content()
    