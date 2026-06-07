using System;
using System.IO;
using System.Threading.Tasks;

using DoomMapGuessr.Services.Cache.Abstractions;

using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Internal;


namespace DoomMapGuessr.Services.Cache
{

    /// <summary>
    /// The caching service used by DoomMapGuessr.
    /// </summary>
    /// <remarks>
    /// Initializes a new caching service.
    /// </remarks>
    /// <param name="cacheDirectory">The directory in which the cache is stored</param>
    public class CachingService(
        string cacheDirectory
    ) : IFullCachingService
    {

        private readonly MemoryCache memory = new(
            new MemoryCacheOptions
            {
                Clock = new SystemClock(),
                CompactionPercentage = 0.5,
                ExpirationScanFrequency = new(0, 3, 0),
                SizeLimit = 1000,
                TrackStatistics = true
            }
        );

        /// <summary>
        /// The directory used for persistent cache.
        /// </summary>
        public string CacheDirectory { get; } = cacheDirectory;

        /// <summary>
        /// The directory used for temporary cache.
        /// </summary>
        public DirectoryInfo TemporaryCacheDirectory { get; } = Directory.CreateDirectory(Path.Join(cacheDirectory, "Temp"));

        /// <summary>
        /// The directory used for persistent cache.
        /// </summary>
        public DirectoryInfo PersistentCacheDirectory { get; } = Directory.CreateDirectory(Path.Join(cacheDirectory, "_Persistent"));

        /// <inheritdoc />
        public void Clear(
            CacheTarget target
        )
        {

            foreach (var flag in Enum.GetValues<CacheTarget>())
            {

                if ((target & flag) == flag)
                    ClearNoFlagSupport(flag);

            }

        }

        /// <summary>
        /// Gets a cached item from memory.
        /// If you wish to get a cached item from
        /// another target, see <see cref="GetString" /> or <see cref="GetBytes" />.
        /// </summary>
        /// <param name="key">The key</param>
        /// <typeparam name="T">The type of data to store</typeparam>
        /// <returns>The value</returns>
        /// <remarks>
        /// For the default caching service, please refrain from using
        /// something other than bytes or strings (unless caching to/from Memory).
        /// </remarks>
        public T? Get<T>(
            string key
        ) =>
            memory.Get<T>(key);

        /// <inheritdoc />
        public string? GetString(
            string key
        )
        {

            if (memory.TryGetValue(key, out string? value))
                return value;

            string pathToTempFile = Path.Join(TemporaryCacheDirectory.FullName, key);

            if (File.Exists(pathToTempFile))
                return File.ReadAllText(pathToTempFile);

            string pathToPersistentFile = Path.Join(PersistentCacheDirectory.FullName, key);

            return File.Exists(pathToPersistentFile)
                       ? File.ReadAllText(pathToPersistentFile)
                       : null;

        }

        /// <inheritdoc />
        public byte[]? GetBytes(
            string key
        )
        {

            if (memory.TryGetValue(key, out byte[]? value))
                return value;

            string pathToTempFile = Path.Join(TemporaryCacheDirectory.FullName, key);

            if (File.Exists(pathToTempFile))
                return File.ReadAllBytes(pathToTempFile);

            string pathToPersistentFile = Path.Join(PersistentCacheDirectory.FullName, key);

            return File.Exists(pathToPersistentFile)
                       ? File.ReadAllBytes(pathToPersistentFile)
                       : null;

        }

        /// <inheritdoc />
        /// <remarks>
        /// If there is a duplicate key, this method will
        /// remove the both the original and the duplicate.
        /// </remarks>
        public void Remove(
            string key
        )
        {

            // btw this method slightly differs
            // as it deletes even if it's already found
            // like lets say there's for some reason
            // the same key in 2 cache storages
            // it'll remove both :)
            string pathToTempFile = Path.Join(TemporaryCacheDirectory.FullName, key);
            string pathToPersistentFile = Path.Join(PersistentCacheDirectory.FullName, key);

            if (memory.TryGetValue<object?>(key, out _))
                memory.Remove(key);

            if (File.Exists(pathToTempFile))
                File.Delete(pathToTempFile);

            if (File.Exists(pathToPersistentFile))
                File.Delete(pathToPersistentFile);

        }

        /// <inheritdoc />
        /// <remarks>
        /// For the default caching service, please refrain from using
        /// something other than bytes or strings (unless caching to/from Memory).
        /// </remarks>
        public void Set<T>(
            string key,
            T value,
            CacheTarget target
        )
        {

            switch (target)
            {

                case CacheTarget.Memory:
                    memory.Set(key, value);

                    return;

                case CacheTarget.Temporary:
                    switch (value)
                    {

                        case string str:
                            File.WriteAllText(Path.Join(TemporaryCacheDirectory.FullName, key), str);

                            return;

                        case byte[] bytes:
                            File.WriteAllBytes(Path.Join(TemporaryCacheDirectory.FullName, key), bytes);

                            return;

                        case StringReader reader:
                            File.WriteAllText(Path.Join(TemporaryCacheDirectory.FullName, key), reader.ReadToEnd());

                            return;

                        default:
                            throw new InvalidOperationException("Cannot use temporary cache with a type other than string or byte[]");

                    }

                case CacheTarget.Persistent:
                    switch (value)
                    {

                        case string str:
                            File.WriteAllText(Path.Join(PersistentCacheDirectory.FullName, key), str);

                            return;

                        case byte[] bytes:
                            File.WriteAllBytes(Path.Join(PersistentCacheDirectory.FullName, key), bytes);

                            return;

                        case StringReader reader:
                            File.WriteAllText(Path.Join(PersistentCacheDirectory.FullName, key), reader.ReadToEnd());

                            return;

                        default:
                            throw new InvalidOperationException("Cannot use temporary cache with a type other than string or byte[]");

                    }

                default:
                    throw new ArgumentOutOfRangeException(nameof(target), target, "Unrecognized cache target");

            }

        }

        /// <inheritdoc />
        public async Task<byte[]?> GetBytesAsync(
            string key
        )
        {

            if (memory.TryGetValue(key, out byte[]? value))
                return value;

            string pathToTempFile = Path.Join(TemporaryCacheDirectory.FullName, key);

            if (File.Exists(pathToTempFile))
                return await File.ReadAllBytesAsync(pathToTempFile);

            string pathToPersistentFile = Path.Join(PersistentCacheDirectory.FullName, key);

            return File.Exists(pathToPersistentFile)
                       ? await File.ReadAllBytesAsync(pathToPersistentFile)
                       : null;

        }

        /// <inheritdoc />
        public async Task<string?> GetStringAsync(
            string key
        )
        {

            if (memory.TryGetValue(key, out string? value))
                return value;

            string pathToTempFile = Path.Join(TemporaryCacheDirectory.FullName, key);

            if (File.Exists(pathToTempFile))
                return await File.ReadAllTextAsync(pathToTempFile);

            string pathToPersistentFile = Path.Join(PersistentCacheDirectory.FullName, key);

            return File.Exists(pathToPersistentFile)
                       ? await File.ReadAllTextAsync(pathToPersistentFile)
                       : null;

        }

        /// <inheritdoc />
        public async Task SetAsync<T>(
            string key,
            T value,
            CacheTarget target
        )
        {

            switch (target)
            {

                case CacheTarget.Temporary:
                    switch (value)
                    {

                        case string str:
                            await File.WriteAllTextAsync(Path.Join(TemporaryCacheDirectory.FullName, key), str);

                            return;

                        case byte[] bytes:
                            await File.WriteAllBytesAsync(Path.Join(TemporaryCacheDirectory.FullName, key), bytes);

                            return;

                        case StringReader reader:
                            await File.WriteAllTextAsync(Path.Join(TemporaryCacheDirectory.FullName, key), await reader.ReadToEndAsync());

                            return;

                        default:
                            throw new InvalidOperationException("Cannot use temporary cache with a type other than string or byte[]");

                    }

                case CacheTarget.Persistent:
                    switch (value)
                    {

                        case string str:
                            await File.WriteAllTextAsync(Path.Join(PersistentCacheDirectory.FullName, key), str);

                            return;

                        case byte[] bytes:
                            await File.WriteAllBytesAsync(Path.Join(PersistentCacheDirectory.FullName, key), bytes);

                            return;

                        case StringReader reader:
                            await File.WriteAllTextAsync(Path.Join(PersistentCacheDirectory.FullName, key), await reader.ReadToEndAsync());

                            return;

                        default:
                            throw new InvalidOperationException("Cannot use temporary cache with a type other than string or byte[]");

                    }

                case CacheTarget.Memory:
                    Set(key, value, CacheTarget.Memory); // no async features available for Memory

                    return;

                default:
                    throw new ArgumentOutOfRangeException(nameof(target), target, "Unrecognized cache target");

            }

        }

        /// <summary>
        /// Clears temporary cache.
        /// </summary>
        private void ClearTemporaryCache()
        {

            foreach (var entry in TemporaryCacheDirectory.EnumerateFileSystemInfos())
                entry.Delete();

        }

        /// <summary>
        /// Clears persistent cache.
        /// </summary>
        private void ClearPersistentCache()
        {

            foreach (var entry in PersistentCacheDirectory.EnumerateFileSystemInfos())
                entry.Delete();

        }

        /// <summary>
        /// Clears a target (does not support bitwise operations).
        /// </summary>
        /// <param name="target">The target</param>
        /// <exception cref="ArgumentOutOfRangeException">Target not recognized</exception>
        private void ClearNoFlagSupport(
            CacheTarget target
        )
        {

            switch (target)
            {

                case CacheTarget.Memory:
                    memory.Clear();

                    break;

                case CacheTarget.Temporary:
                    ClearTemporaryCache();

                    break;

                case CacheTarget.Persistent:
                    ClearPersistentCache();

                    break;

                default:
                    throw new ArgumentOutOfRangeException(nameof(target), target, "No such cache target");

            }

        }

        /// <inheritdoc cref="Remove" />
        public void Delete(
            string key
        ) =>
            Remove(key);

    }

}
