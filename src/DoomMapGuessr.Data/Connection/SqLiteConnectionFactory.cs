using Microsoft.Data.Sqlite;


namespace DoomMapGuessr.Data.Connection;


    /// <summary>
    /// Factory responsible for creating connections to SQLite databases.
    /// </summary>
    /// <remarks>
    /// Initializes a new factory responsible for creating
    /// connections to SQLite databases.
    /// </remarks>
    /// <param name="connectionString">The connection string</param>
    public class SqLiteConnectionFactory(string? connectionString) : ISqLiteConnectionFactory
    {

        /// <inheritdoc />
        public SqliteConnection CreateConnection() => new(connectionString);

    }
