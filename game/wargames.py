import random
from typing import Dict

class WarGames:
    """Thermo Nuclear War mini-game from War Games"""
    
    @staticmethod
    def play() -> str:
        """Play a round of Thermo Nuclear War"""
        output = []
        output.append("═══════════════════════════════════════")
        output.append("    THERMO NUCLEAR WAR")
        output.append("═══════════════════════════════════════")
        output.append("")
        output.append("A strange game. The only winning move")
        output.append("is not to play. How about a nice game")
        output.append("of chess?")
        output.append("")
        output.append("...but since you're here:")
        output.append("")
        
        # Simple version: player picks a country, computer picks one
        # Both launch nukes, see who survives
        countries = [
            "United States", "Soviet Union", "China", 
            "United Kingdom", "France", "Germany",
            "Japan", "India", "Pakistan", "Israel"
        ]
        
        # Random outcome
        player_country = random.choice(countries)
        enemy_country = random.choice([c for c in countries if c != player_country])
        
        output.append(f"Player launches from: {player_country}")
        output.append(f"Enemy launches from: {enemy_country}")
        output.append("")
        
        # Roll for outcome
        player_roll = random.randint(1, 20)
        enemy_roll = random.randint(1, 20)
        
        output.append(f"{player_country} rolls: {player_roll}")
        output.append(f"{enemy_country} rolls: {enemy_roll}")
        output.append("")
        
        if player_roll > enemy_roll:
            output.append("💥 You win! But at what cost?")
            output.append("The world burns in nuclear fire.")
        elif enemy_roll > player_roll:
            output.append("💥 You lose! Nuclear winter descends.")
            output.append("There are no winners in nuclear war.")
        else:
            output.append("💥 Mutual destruction!")
            output.append("Both sides are annihilated.")
        
        output.append("")
        output.append("═══════════════════════════════════════")
        output.append("Would you like to play again?")
        output.append("(Type 'wargames' to play again)")
        output.append("═══════════════════════════════════════")
        
        return '\n'.join(output)

