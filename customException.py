from typing import Any
import pickle


class HardwareError(Exception):
    def __init__(self, message: str, value: Any) -> None:
        super().__init__(message)
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f'{self.__class__, (self.message, self.value)}'
   
    def __repr__(self) -> str:
        return f'HardwareError(message={self.message!r}, value={self.value!r})'     
    
    
    def __reduce__(self) -> tuple[Any, tuple[str, Any]]:
        return (self.__class__, (self.message, self.value)) 
    
overheated_exception: HardwareError = HardwareError(message='Computer is overheating', value=137)
print(overheated_exception)
print(repr(overheated_exception))
print(overheated_exception.message)
print(overheated_exception.value)

try:
    raise HardwareError(message='Laptop is too hot', value=101)
except HardwareError as e:
    print(e)

OE: HardwareError = HardwareError(message='Overheating detected', value =101)
print(repr(OE))
pickled: bytes = pickle.dumps(OE)
unpickled: HardwareError = pickle.loads(pickled)
print(repr(unpickled))
print(unpickled.message)
print(unpickled.value)    