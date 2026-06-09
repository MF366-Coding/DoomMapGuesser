using System;

using CommunityToolkit.Mvvm.Input;

using DoomMapGuessr.Helpers;
using DoomMapGuessr.Strings;

using Octokit;


namespace DoomMapGuessr.ViewModels
{

    public partial class HomePageViewModel : ViewModelBase
    {

        private readonly string[] greetings = [Resources.Greetings_Regular01, Resources.Greetings_Regular02];

        private readonly Random random = new();

        /// <summary>
        /// Initializes the home page view model.
        /// </summary>
        public HomePageViewModel() { }

        /// <summary>
        /// Release body to display under the "What's new?" widget.
        /// </summary>
        public static string LatestReleaseBody { get; } = ApplicationServices.SavedRelease?.Body is null
                                                              ? "# No release data found.\nSomething went wrong."
                                                              : ApplicationServices.SavedRelease.TagName[1..] ==
                                                                ApplicationServices.VersionInfo.ApplicationVersion
                                                                  ? $"# What's new in this version?\n**DoomMapGuessr {ApplicationServices.SavedRelease.TagName}**\n\n{ApplicationServices.SavedRelease.Body}"
                                                                  : ApplicationServices.VersionInfo
                                                                                       .IsDevVersion // now we actually have a property named
                                                                                                     // "IsDevVersion" how fucking cool right?
                                                                      ? "# No release data found.\nIt seems this is a build contained in a developer channel of DoomMapGuessr. If you are not a tester nor a developer, it is recommended you update to the latest stable version."
                                                                      : $"# New version available! What's new?\n**DoomMapGuessr {ApplicationServices.SavedRelease.TagName}**\n\n{ApplicationServices.SavedRelease.Body}";

        /// <summary>
        /// The random (or not so random) greeting chosen
        /// to be displayed in the home page.
        /// </summary>
        public string RandomGreeting =>
            DateTime.Now.Hour switch
            {

                3 => Resources.Greetings_CreepyHour01,
                18 or 19 => Resources.Greetings_Sunset01,
                _ => random.GetItems(greetings, 1)[0]

            };

        [RelayCommand]
        private void NavigateToUnlockables() => ApplicationServices.NavigationService.NavigateTo("AchievementsUnlockables");

        [RelayCommand]
        private void NavigateToClassicMode() => ApplicationServices.NavigationService.NavigateTo("ClassicMode");

        [RelayCommand]
        private void OpenGitHubRepo()
        {

            if (ApplicationServices.Get<Release>().HtmlUrl is null)
                return;

            _ = WebBrowser.OpenUrl(ApplicationServices.Get<Release>().HtmlUrl);

        }

    }

}
