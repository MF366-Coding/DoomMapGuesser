using System.Threading.Tasks;


namespace DoomMapGuessr.Services.Settings
{

    /// <summary>
    /// Abstraction for a service that stores and loads settings.
    /// </summary>
    public interface ISettingsService
    {

        /// <summary>
        /// Adds a value to storage. If the value is already
        /// stored, throws an error.
        /// </summary>
        /// <typeparam name="T">The type of the value</typeparam>
        /// <param name="key">The key</param>
        /// <param name="value">The value to store</param>
        void Add<T>(
            string key,
            T value
        );

        /// <summary>
        /// Checks if a given key exists in storage.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns><c>true</c> if it exists</returns>
        bool Contains(
            string key
        );

        /// <summary>
        /// Gets a stored value.
        /// </summary>
        /// <typeparam name="T">The type of the value</typeparam>
        /// <param name="key">The key</param>
        /// <param name="defaultValue">The value to default to</param>
        /// <returns>The stored value or <paramref name="defaultValue" /></returns>
        T Get<T>(
            string key,
            T defaultValue = default!
        );

        /// <summary>
        /// Gets a stored boolean.<br />
        /// <c>1</c>, <c>true</c> (case-insensitive),
        /// <c>1.0</c> are all considered "truths".<br />
        /// Lack of value is considered "falsy".
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The boolean</returns>
        bool GetBoolean(
            string key
        );

        /// <summary>
        /// Gets a stored double.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The double</returns>
        double GetDouble(
            string key
        );

        /// <summary>
        /// Gets a stored integer.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The integer</returns>
        int GetInt32(
            string key
        );

        /// <summary>
        /// Gets a stored long integer.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The long integer</returns>
        long GetInt64(
            string key
        );

        /// <summary>
        /// Gets a stored string.
        /// </summary>
        /// <param name="key">The key</param>
        /// <returns>The string or <c>null</c></returns>
        string? GetString(
            string key
        );

        /// <summary>
        /// Saves the settings.
        /// </summary>
        void Save();

        /// <summary>
        /// Saves the settings async.
        /// </summary>
        /// <returns></returns>
        Task SaveAsync();

        /// <summary>
        /// Adds or overwrites a value.
        /// </summary>
        /// <typeparam name="T">The type of the value</typeparam>
        /// <param name="key">The key</param>
        /// <param name="value">The value to store</param>
        void Set<T>(
            string key,
            T value
        );

        /// <summary>
        /// Tries to get a stored value.
        /// </summary>
        /// <typeparam name="T">The type of the value</typeparam>
        /// <param name="key">The key</param>
        /// <param name="value">The returned value</param>
        /// <returns><c>true</c> if found</returns>
        bool TryGet<T>(
            string key,
            out T value
        );

    }

}
