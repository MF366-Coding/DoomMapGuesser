using System;


namespace DoomMapGuessr.Services.Cache
{

    /// <summary>
    /// The target for a cache operation.
    /// </summary>
    [Flags]
    public enum CacheTarget
    {

        /// <summary>
        /// Caches only while the app is running.
        /// </summary>
        Memory = 1,

        /// <summary>
        /// Caches temporarily, cleared on defined
        /// schedule / app closed.
        /// </summary>
        Temporary = 2,

        /// <summary>
        /// Persistent cache.
        /// </summary>
        Persistent = 4

    }

}
