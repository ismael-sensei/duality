from domain.entities import Tracker
from domain.interfaces import TrackerRepository, CacheRepository


class CachedTrackerRepository(TrackerRepository):
    def __init__(self, cache_repo: CacheRepository):
        self.cache_repo = cache_repo

    def set_tracker(self, tracker_id: str, tracker: Tracker):
        self.cache_repo.set(f"Tracker:{tracker_id}", tracker)

    def get_tracker(self, tracker_id: str) -> Tracker:
        tracker: Tracker = self.cache_repo.get(f"Tracker:{tracker_id}", Tracker)

        if tracker:
            return tracker
        else:
            return None
        
    def del_tracker(self, tracker_id: str):
        self.cache_repo.delete(tracker_id)
    


