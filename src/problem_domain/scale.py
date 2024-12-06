class Scale:
    def __init__(self):
        self._local_player_points = 0
        self._remote_player_points = 0

    def add_points(self, points: int, player: str):
        if player == "local":
            self._local_player_points += points
        elif player == "remote":
            self._remote_player_points += points
        else:
            raise ValueError("Invalid player")
    
    def check_for_winner(self):
        pass
        
    def calcule_points_difference(local_player_points : int, remote_player_points : int):
        return local_player_points - remote_player_points