namespace DoomMapGuessr.Data.Entities
{

    /// <summary>
    /// Map in an episode in a game of the DOOM series.
    /// </summary>
    /// <param name="Id">Map ID</param>
    /// <param name="Title">Map title/name</param>
    /// <param name="RelativePosition">Position of map in episode</param>
    /// <param name="SecretCount">Amount of secrets in map</param>
    /// <param name="DifficultyModifier">Difficulty modifier for all images in this map</param>
    /// <param name="IsHellKeepInEpisode">Boolean: whether this map is 'Hell Keep'-like in the episode it is contained in</param>
    /// <param name="IsWarrensInEpisode">Boolean: whether this map is 'Warrens'-like in the episode it is contained in</param>
    /// <param name="AutomapViewSource">Source of the automap view of this map</param>
    /// <param name="EpisodeId">ID of episode that contains this map</param>
    public record Map(
        int Id,
        string Title,
        int RelativePosition,
        int SecretCount,
        int DifficultyModifier,
        int IsHellKeepInEpisode,
        int IsWarrensInEpisode,
        string? AutomapViewSource,
        int EpisodeId
    );

}
