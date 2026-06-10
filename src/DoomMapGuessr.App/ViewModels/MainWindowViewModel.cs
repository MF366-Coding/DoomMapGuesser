using Avalonia.Controls;

using CommunityToolkit.Mvvm.ComponentModel;

using DoomMapGuessr.Services;
using DoomMapGuessr.Views;


namespace DoomMapGuessr.ViewModels
{

    /// <summary>
    /// View model for the <see cref="MainWindow" />.
    /// </summary>
    public partial class MainWindowViewModel : ViewModelBase,
                                               INavigationService
    {

        /// <summary>
        /// Initializes the ViewModel for the <see cref="MainWindow" />.
        /// </summary>
        public MainWindowViewModel() =>
            CurrentPage = new HomePage
            {
                DataContext = ApplicationServices.Get<HomePageViewModel>()
            };

        [ObservableProperty]
        public partial UserControl CurrentPage { get; set; }

        [ObservableProperty]
        public partial bool IsSidebarOpen { get; set; } = true;

        /// <inheritdoc />
        public void NavigateTo(
            string pageName
        )
        {

            switch (pageName)
            {

                case "Home":
                    CurrentPage = new HomePage
                    {
                        DataContext = ApplicationServices.Get<HomePageViewModel>()
                    };

                    break;

                case "ClassicMode":
                    CurrentPage = new ClassicModePage
                    {
                        DataContext = ApplicationServices.Get<ClassicModeViewModel>()
                    };

                    break;

                case "PrecisionMode":
                    CurrentPage = new PrecisionModePage
                    {
                        DataContext = ApplicationServices.Get<PrecisionModeViewModel>()
                    };

                    break;

                case "AchievementsUnlockables":
                    CurrentPage = new AchievementsUnlockablesPage
                    {
                        DataContext = ApplicationServices.Get<AchievementsUnlockablesViewModel>()
                    };

                    break;

                case "Settings":
                    CurrentPage = new SettingsPage
                    {
                        DataContext = ApplicationServices.Get<SettingsPageViewModel>()
                    };

                    break;

                case "CloseSidebarPane":
                    IsSidebarOpen = false;

                    break;

                case "OpenSidebarPane":
                    IsSidebarOpen = true;

                    break;

                case "ToggleSidebarPane":
                    IsSidebarOpen = !IsSidebarOpen;

                    break;

            }

        }

        /// <inheritdoc />
        public void NavigateTo(
            string pageName,
            object? parameter
        ) =>
            NavigateTo(pageName);

    }

}
