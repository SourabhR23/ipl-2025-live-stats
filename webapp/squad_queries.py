def squad_tb(team):
    return f"""
            SELECT 
                teamName, 
                shortname, 
                playerName, 
                role, 
                battingStyle, 
                bowlingStyle, 
                country
            FROM squad_df
            WHERE teamName = "{team}";
        """