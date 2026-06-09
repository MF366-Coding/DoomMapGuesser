namespace DoomMapGuessr.Data.Entities
{

    /// <summary>
    /// Game in the DOOM series.
    /// </summary>
    /// <param name="Id">Game ID</param>
    /// <param name="Title">Game title</param>
    /// <param name="YearOfRelease">Year of game's release</param>
    public record Game(
        int Id,
        string Title,
        string YearOfRelease
    );

}
