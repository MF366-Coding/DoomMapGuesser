using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;


namespace DoomMapGuessr.Helpers
{

    /// <summary>
    /// Helper class for fetching the DoomMapGuessr official database, as well the DOLU file.
    /// </summary>
    public static class DatabaseFetcher
    {

        private static readonly HttpClient client = new();

        /// <summary>
        /// Fetches the database.
        /// </summary>
        /// <param name="url">The database URL</param>
        /// <param name="token">The <see cref="CancellationToken" /></param>
        /// <returns>Information containing status code and data regarding the database</returns>
        public static async Task<HttpResponseMessage> FetchAsync(
            string url,
            CancellationToken token
        ) =>
            await client.GetAsync(url, HttpCompletionOption.ResponseContentRead, token);

        /// <summary>
        /// Fetches the database as a <see cref="Stream" />.
        /// </summary>
        /// <param name="url">The database URL</param>
        /// <param name="token">The <see cref="CancellationToken" /></param>
        /// <returns>The database</returns>
        public static async Task<Stream> FetchStreamAsync(
            string url,
            CancellationToken token
        ) =>
            await client.GetStreamAsync(url, token);

        /// <summary>
        /// Fetches the database as a bytearray.
        /// </summary>
        /// <param name="url">The database URL</param>
        /// <param name="token">The <see cref="CancellationToken" /></param>
        /// <returns>The database</returns>
        public static async Task<byte[]> FetchBytesAsync(
            string url,
            CancellationToken token
        ) =>
            await client.GetByteArrayAsync(url, token);

        /// <summary>
        /// Fetches the database as a string.
        /// </summary>
        /// <param name="url">The database URL</param>
        /// <param name="token">The <see cref="CancellationToken" /></param>
        /// <returns>The database</returns>
        public static async Task<string> FetchStringAsync(
            string url,
            CancellationToken token
        ) =>
            await client.GetStringAsync(url, token);

    }

}
