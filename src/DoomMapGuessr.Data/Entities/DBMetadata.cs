namespace DoomMapGuessr.Data.Entities;


    /// <summary>
    /// Database metadata.
    /// </summary>
    /// <param name="DBTitle">Database title</param>
    /// <param name="DBAuthor">Database author</param>
    /// <param name="DBVersion">Database version</param>
    /// <param name="DBDateOfLastUpdate">Date of the last update to the database</param>
    /// <param name="DBOfficialDownloadLink">Official link to download the database</param>
    /// <param name="DBSources">Sources where screenshots were taken from</param>
    /// <param name="DBReviewer">Database reviewer</param>
    /// <param name="DBCompatibilityData">List of DoomMapGuessr versions that offer compatibility with the database</param>
    /// <param name="DBOtherMetadata">Mixed metadata</param>
    public record DBMetadata(
        string DBTitle,
        string DBAuthor,
        int DBVersion,
        string DBDateOfLastUpdate,
        string? DBOfficialDownloadLink,
        string? DBSources,
        string? DBReviewer,
        string? DBCompatibilityData,
        string? DBOtherMetadata
    );
