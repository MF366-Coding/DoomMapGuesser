namespace DoomMapGuessr.Data.Entities
{

    /// <summary>
    /// Episode of a game in the DOOM series.
    /// </summary>
    /// <param name="Id">Episode ID</param>
    /// <param name="Title">Episode name/title</param>
    /// <param name="RelativePosition">Position of episode in game</param>
    /// <param name="GameId">ID of game that contains the episode</param>
    public record Episode(
        int Id,
        string Title,
        int RelativePosition,
        int GameId
    );

}
