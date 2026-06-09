using System.Threading.Tasks;


namespace DoomMapGuessr.Services.Cache.Abstractions
{

    /// <summary>
    /// An asynchronous caching service.
    /// </summary>
    public interface ICachingServiceAsync
    {

        /// <summary>
        /// Gets a cached bytearray async.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The bytearray</returns>
        Task<byte[]?> GetBytesAsync(
            string key
        );

        /// <summary>
        /// Gets a cached string async.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The string</returns>
        Task<string?> GetStringAsync(
            string key
        );

        /// <summary>
        /// Caches an item async.
        /// </summary>
        /// <param name="key">The key</param>
        /// <param name="value">The value to cache</param>
        /// <param name="target">The cache location</param>
        /// <typeparam name="T">The type</typeparam>
        /// <returns></returns>
        Task SetAsync<T>(
            string key,
            T value,
            CacheTarget target
        );

    }

}
