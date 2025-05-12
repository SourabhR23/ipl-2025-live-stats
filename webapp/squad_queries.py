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

def all_squad():
    return """
        SELECT * FROM squad_df;
        """

def all_bowling():
    return """
        SELECT * FROM bowling_df;
        """

def all_batting():
    return """
        SELECT * FROM batting_df;
        """