using Microsoft.Data.Sqlite;


namespace DoomMapGuessr.Data.Connection
{

    /// <summary>
    /// Factory responsible for creating connections to SQLite databases.
    /// </summary>
    public interface ISqLiteConnectionFactory
    {

        /// <summary>
        /// Creates a connection to a SQLite database.
        /// </summary>
        /// <returns>The connection</returns>
        SqliteConnection CreateConnection();

    }

}
