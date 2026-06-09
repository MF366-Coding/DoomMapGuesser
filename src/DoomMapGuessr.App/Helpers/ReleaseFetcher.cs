using System.Threading.Tasks;

using Octokit;


namespace DoomMapGuessr.Helpers
{

    /// <summary>
    /// Helper class for fetching GitHub Releases.
    /// </summary>
    public static class ReleaseFetcher
    {

        private static readonly GitHubClient client = new(new ProductHeaderValue("DoomMapGuessr"));

        /// <summary>
        /// Fetches a release from a repository given its tag.
        /// </summary>
        /// <param name="owner">The repository owner</param>
        /// <param name="repo">The repository name</param>
        /// <param name="tag">The release tag</param>
        /// <returns>The release</returns>
        public static async Task<Release> FetchAsync(
            string owner,
            string repo,
            string tag
        ) =>
            await client.Repository.Release.Get(owner, repo, tag);

        /// <summary>
        /// Fetches the latest release from a repository.
        /// </summary>
        /// <param name="owner">The repository owner</param>
        /// <param name="repo">The repository name</param>
        /// <returns>The release</returns>
        public static Release FetchLatest(
            string owner,
            string repo
        ) =>
            client.Repository.Release.GetLatest(owner, repo).Result;

        /// <summary>
        /// Fetches the latest release from a repository.
        /// </summary>
        /// <param name="owner">The repository owner</param>
        /// <param name="repo">The repository name</param>
        /// <returns>The release</returns>
        public static async Task<Release> FetchLatestAsync(
            string owner,
            string repo
        ) =>
            await client.Repository.Release.GetLatest(owner, repo);

    }

}
