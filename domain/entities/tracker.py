from dataclasses import dataclass

@dataclass
class Tracker:
    _tokens: int
    max_tokens: int

    def __post_init__(self):
        self.tokens = self._tokens

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value: int):
        self._tokens = max(min(value, self.max_tokens), 0)
        
