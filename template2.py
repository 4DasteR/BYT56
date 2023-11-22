from abc import ABC, abstractmethod
from typing import List, Dict

class SequenceTemplate(ABC):
    sequence: List = []
    
    def template_method(self) -> None:
        self.generate()
        self.print()
        
    def print(self) -> None:
        print(' '.join([str(i) for i in self.sequence]))
     
    @abstractmethod       
    def generate(self, n: int) -> None:
        pass
    
class FibonacciSequence(SequenceTemplate):
    def __init__(self):
        self.memo: Dict[int, int] = {}

    def generate(self, n: int) -> None:
        self.sequence = [self.fibonacci(i) for i in range(n)]

    def fibonacci(self, n: int) -> int:
        if n <= 1:
            return n
        elif n not in self.memo:
            self.memo[n] = self.fibonacci(n - 1) + self.fibonacci(n - 2)
        return self.memo[n]
    
class CharSequence(SequenceTemplate):
    def generate(self, n: int) -> None:
        self.sequence = [chr(ord('A') + i) for i in range(n)]
        
if __name__ == '__main__':
    fib: SequenceTemplate = FibonacciSequence()
    char: SequenceTemplate = CharSequence()
    
    fib.generate(10)
    fib.print()
    
    char.generate(7)
    char.print()