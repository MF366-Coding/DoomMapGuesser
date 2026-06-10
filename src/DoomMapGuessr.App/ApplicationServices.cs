using System;

using DoomMapGuessr.Models;
using DoomMapGuessr.Services;
using DoomMapGuessr.ViewModels;

using Microsoft.Extensions.DependencyInjection;

using Octokit;


namespace DoomMapGuessr
{

    /// <summary>
    /// Helper class for getting required services (DI).
    /// </summary>
    public static class ApplicationServices
    {

        /// <summary>
        /// The Service Provider.
        /// </summary>
        public static IServiceProvider Root { get; internal set; } = null!;

        /// <summary>
        /// The version information for this application.
        /// </summary>
        public static ApplicationVersioningInformation VersionInfo { get; internal set; } = null!;

        /// <summary>
        /// The latest GitHub release.
        /// </summary>
        public static Release? SavedRelease { get; internal set; } = null;

        /// <summary>
        /// Gets a required service.
        /// </summary>
        /// <remarks>Type constraint is <c>notnull</c></remarks>
        /// <typeparam name="T">The type of service</typeparam>
        /// <returns>The service</returns>
        public static T Get<T>()
            where T : notnull =>
            typeof(T) is null ? throw new NullReferenceException($"Service {typeof(T).FullName} is null") : Root.GetRequiredService<T>();

    }

}
