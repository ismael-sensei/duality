from adapter.gateways.cache import CachedTrackerRepository
from domain.entities import Tracker

class TrackerInteractor():
    tracker_id: str
    repo: CachedTrackerRepository
    tracker: Tracker

    def __init__(self, game_id: str, tracker_id: str, repo: CachedTrackerRepository):
        self.tracker_id = f'{game_id}-{tracker_id}'
        self.repo = repo
        self.tracker = self.repo.get_tracker(self.tracker_id)

    def create_tracker(self, tokens = 0, max_tokens = 100):
        self.tracker = Tracker(_tokens = tokens, max_tokens= max_tokens)
        self.repo.set_tracker(self.tracker_id, self.tracker)
        return self.tracker
    
    def add_tokens(self, tokens = 1):
        self.tracker.tokens = self.tracker.tokens + tokens
        self.repo.set_tracker(self.tracker_id, self.tracker)
        return self.tracker
    
    def set_tokens(self, tokens = 0):
        self.tracker.tokens = tokens
        self.repo.set_tracker(self.tracker_id, self.tracker)
        return self.tracker

    def del_tracker(self):
        self.repo.del_tracker(self.tracker_id)