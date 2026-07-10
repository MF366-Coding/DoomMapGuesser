namespace DoomMapGuessr.Services.Cache.Abstractions;


    /// <summary>
    /// A synchronous caching service.
    /// </summary>
    public interface ICachingService
    {

        /// <summary>
        /// Clears one or multiple cache location (bitwise operations).
        /// </summary>
        /// <param name="target">The target</param>
        void Clear(
            CacheTarget target
        );

        /// <summary>
        /// Determines, given a key, whether the key-value pair exists.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns><c>true</c> if the pair exists in cache</returns>
        bool Exists(
            string key
        );

        /// <summary>
        /// Gets a cached item.
        /// </summary>
        /// <param name="key">The key</param>
        /// <typeparam name="T">The type of data to store</typeparam>
        /// <returns>The value</returns>
        T? Get<T>(
            string key
        );

        /// <summary>
        /// Gets a cached string.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The string</returns>
        string? GetString(
            string key
        );

        /// <summary>
        /// Gets a cached bytearray.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The bytearray</returns>
        byte[]? GetBytes(
            string key
        );

        /// <summary>
        /// Removes something from cache.
        /// </summary>
        /// <param name="key">The key</param>
        void Remove(
            string key
        );

        /// <summary>
        /// Caches an item.
        /// </summary>
        /// <param name="key">The key</param>
        /// <param name="value">The value to cache</param>
        /// <param name="target">The cache location</param>
        /// <typeparam name="T">The type</typeparam>
        void Set<T>(
            string key,
            T value,
            CacheTarget target
        );

    }
