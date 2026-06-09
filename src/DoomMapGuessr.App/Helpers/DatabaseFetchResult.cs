namespace DoomMapGuessr.Helpers
{

    /// <summary>
    /// Possible outcomes of fetching the database.
    /// </summary>
    public enum DatabaseFetchResult
    {

        /// <summary>
        /// Used the cache, did not check the
        /// database.
        /// </summary>
        NoCheckAndCache,

        /// <summary>
        /// Checked the database, did not cache.
        /// </summary>
        CheckNoCache,

        /// <summary>
        /// Checked the database and cached it.
        /// </summary>
        CheckAndCache,

        /// <summary>
        /// There was an error during checking,
        /// but cache was available and used.
        /// </summary>
        CheckErrorAndCache,

        /// <summary>
        /// There was an error during checking
        /// and cache was NOT available.
        /// </summary>
        CheckErrorNoCache

    }

}
