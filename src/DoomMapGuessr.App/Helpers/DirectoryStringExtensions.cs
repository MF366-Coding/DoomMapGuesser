using System.Collections.Generic;
using System.IO;


namespace DoomMapGuessr.Helpers;


    /// <summary>
    /// Generic extensions for <see cref="System.String" />s that represent directory paths.
    /// </summary>
    internal static class DirectoryStringExtensions
    {

        /// <summary>
        /// Enumerates subdirectories in a directory.
        /// </summary>
        /// <returns>An enumerable of directory paths</returns>
        internal static IEnumerable<string> EnumerateDirectories(
            this string directory
        ) =>
            Directory.EnumerateDirectories(directory);

        /// <summary>
        /// Enumerates files in a directory.
        /// </summary>
        /// <returns>An enumerable of filepaths</returns>
        internal static IEnumerable<string> EnumerateFiles(
            this string directory
        ) =>
            Directory.EnumerateFiles(directory);

    }
