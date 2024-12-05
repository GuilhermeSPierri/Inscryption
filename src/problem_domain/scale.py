

class Scale:

    def __init__(self):
        self.local_player_points = 0
        self.remote_player_points = 0

    def add_points(self, points: int, player: str):
        if player == "local":
            self.local_player_points += points
        elif player == "remote":
            self.remote_player_points += points
        else:
            raise ValueError("Invalid player")
    
    def check_winner(self):
        if self.local_player_points - self.remote_player_points >= 7:
            return "local"
        elif self.remote_player_points - self.local_player_points >= 7:
            return "remote"
        else:
            return ""