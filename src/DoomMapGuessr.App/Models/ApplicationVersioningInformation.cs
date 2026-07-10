using System;
using System.Reflection;


namespace DoomMapGuessr.Models;


    /// <summary>
    /// An immutable data structure containing information on an application's versioning.
    /// </summary>
    public record ApplicationVersioningInformation
    {

        /// <summary>
        /// Initializes a new instance of the
        /// <see cref="ApplicationVersioningInformation" />
        /// class.
        /// </summary>
        /// <param name="assembly">The assembly where the version information is located</param>
        public ApplicationVersioningInformation(
            Assembly? assembly
        )
        {

            AssemblyVersion = assembly?.GetName().Version;

            ApplicationVersion = AssemblyVersion is null
                                     ? null
                                     : $"{AssemblyVersion.Major}{AssemblyVersion.Minor}{AssemblyVersion.Build}";

        }

        /// <summary>
        /// The version of the Assembly.
        /// </summary>
        public Version? AssemblyVersion { get; }

        /// <summary>
        /// The application version.
        /// </summary>
        public string? ApplicationVersion { get; }

        /// <summary>
        /// Whether or not this version matches a dev version (alpha, beta, dev...).
        /// </summary>
        public bool IsDevVersion => AssemblyVersion?.Revision == 1;

    }
