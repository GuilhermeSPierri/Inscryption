class Scale:
    def __init__(self):
        self._local_player_points = 0
        self._remote_player_points = 0

    def add_points(self, points: int, player_field):

        if player_field == "local":
            self._remote_player_points += points
        else:
            raise ValueError("Invalid player")
                
    def calcule_points_difference(self):
        return self._local_player_points - self._remote_player_points

    def set_local_player_points(self, points: int):
        self._local_player_points = points

    def set_remote_player_points(self, points: int):
        self._remote_player_points = points