class Pupil:
    def __init__(self, postcode: str, will_join_others: bool, will_share_others: bool, spare_seats: int):
        '''
        needs lat and long using apis and stuff
        '''
        self.postcode: str = postcode
        self.will_join_others: bool = will_join_others
        self.will_share_others: bool = will_share_others
        self.spare_seats: int = spare_seats
