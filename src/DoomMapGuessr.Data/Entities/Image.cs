namespace DoomMapGuessr.Data.Entities;


    /// <summary>
    /// Screenshot of a part of a map in a DOOM game.
    /// </summary>
    /// <param name="Id">Screenshot ID</param>
    /// <param name="Source">Screenshot source (usually URL)</param>
    /// <param name="DifficultyLevel">Screenshot difficulty level</param>
    /// <param name="X">Screenshot coordinates: X</param>
    /// <param name="Y">Screenshot coordinates: Y</param>
    /// <param name="Z">Screenshot coordinates: Z</param>
    /// <param name="MapId">ID of the map where this screenshot was taken</param>
    public record Image(
        int Id,
        string Source,
        int DifficultyLevel,
        double X,
        double Y,
        double Z,
        int MapId
    );
