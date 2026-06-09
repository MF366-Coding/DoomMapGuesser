using System;
using System.Globalization;

using Avalonia;
using Avalonia.Styling;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using DoomMapGuessr.Services.Settings;
using DoomMapGuessr.Strings;


namespace DoomMapGuessr.ViewModels
{

    public partial class SettingsPageViewModel : ViewModelBase
    {

        [ObservableProperty]
        public partial int CurrentIndex { get; set; } = Array.IndexOf(
            App.AllowedCultures, ApplicationServices.Get<ISettingsService>()
                                                    .GetString("Language.Culture")
        );

        [ObservableProperty]
        public partial int Proportions { get; set; } = Math.Min(
            Math.Clamp(
                ApplicationServices.Get<ISettingsService>().GetInt32("Screenshots.Proportions"),
                0, 3
            ),
            0
        );

        [ObservableProperty]
        public partial bool CustomTheme { get; set; } = !ApplicationServices.Get<ISettingsService>()
                                                                            .GetBoolean("GUI.FollowSystem");

        [ObservableProperty]
        public partial bool DarkTheme { get; set; } = ApplicationServices.Get<ISettingsService>()
                                                                         .GetBoolean("GUI.DarkTheme");

        [ObservableProperty]
        public partial string[] LanguageComboBoxItems { get; set; } =
        [

			// The comments to the right of the items
			// are easy ways to match languages to codes.
			// Item: Native name
			// In comment, by this order:
			// English name, ISO language name (2 letters),
			// ISO language name (3 letters),
			// Windows (3 letter language name), Windows LCID
			Resources.Settings_Language_FollowSystem, // Same as System (Not Invariant)
			"English (United States)",                // English (United States)			// en // eng // ENU // 1033
			"Português (Brasil)",                     // Portuguese (Brazil)				// pt // por // PTB // 1046
			"Português (Portugal)"                    // Portuguese (Portugal)			// pt // por // PTG // 2070

		];

        private void RunLanguageChangeProtocol()
        {

            string culture = CurrentIndex == 0 // same as system
                                 ? App.AllowedCultures.Contains(
                                       CultureInfo.CurrentCulture.Name, StringComparer.OrdinalIgnoreCase
                                   )                                     // same as system is allowed
                                       ? CultureInfo.CurrentCulture.Name // same as system
                                       : App.AllowedCultures[1]          // en-US
                                 : App.AllowedCultures[CurrentIndex];

            Resources.Culture = new(culture); // auto updates UI
            CultureInfo.CurrentCulture = Resources.Culture;

            ApplicationServices.Get<ISettingsService>().Set("Language.Culture", culture);

        }

        private void RunThemeChangeProtocol()
        {

            ApplicationServices.Get<ISettingsService>()
                               .Set(
                                   "GUI.FollowSystem", CustomTheme
                                                           ? "0"
                                                           : "1"
                               );

            ApplicationServices.Get<ISettingsService>()
                               .Set(
                                   "GUI.DarkTheme", CustomTheme
                                                        ? "1"
                                                        : "0"
                               );

            _ = Application.Current?.RequestedThemeVariant = !CustomTheme
                                                                 ? ThemeVariant.Default
                                                                 : DarkTheme
                                                                     ? ThemeVariant.Dark
                                                                     : ThemeVariant.Light;

        }

        [RelayCommand]
        private void SaveSettings()
        {

            RunLanguageChangeProtocol();
            RunThemeChangeProtocol();
            ApplicationServices.Get<ISettingsService>().Save();

        }

    }

}
