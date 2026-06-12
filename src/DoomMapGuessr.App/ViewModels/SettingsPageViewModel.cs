using System;
using System.Globalization;

using Avalonia;
using Avalonia.Styling;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using DoomMapGuessr.Enums;
using DoomMapGuessr.Services.Settings;
using DoomMapGuessr.Strings;


namespace DoomMapGuessr.ViewModels
{

    public partial class SettingsPageViewModel : ViewModelBase
    {

        [ObservableProperty]
        public partial int Language_CurrentIndex { get; set; } = Array.IndexOf(
            App.AllowedCultures, ApplicationServices.Get<ISettingsService>()
                                                    .GetString("Language.Culture")
        );

        [ObservableProperty]
        public partial AspectRatio Screenshots_AspectRatio { get; set; } = (AspectRatio)Math.Clamp(
            ApplicationServices.Get<ISettingsService>().GetInt32("Screenshots.AspectRatio"),
            0, 3
        );

        [ObservableProperty]
        public partial bool GUI_CustomTheme { get; set; } = !ApplicationServices.Get<ISettingsService>()
                                                                            .GetBoolean("GUI.FollowSystem");

        [ObservableProperty]
        public partial bool GUI_DarkTheme { get; set; } = ApplicationServices.Get<ISettingsService>()
                                                                         .GetBoolean("GUI.DarkTheme");

        [ObservableProperty]
        public partial string[] Language_ComboBoxItems { get; set; } =
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
            "Português (Portugal)"                    // Portuguese (Portugal)			    // pt // por // PTG // 2070

        ];

        [ObservableProperty]
        public partial ColorBlindness Screenshots_ColorBlindness { get; set; } = (ColorBlindness)Math.Clamp(
            ApplicationServices.Get<ISettingsService>().GetInt32("Screenshots.ColorBlindness"),
            0, 4
        );

        [ObservableProperty]
        public partial bool Screenshots_BlacklistIsWhitelist { get; set; } = ApplicationServices.Get<ISettingsService>().GetBoolean("Screenshots.BlacklistIsWhitelist");


		private void RunLanguageChangeProtocol(ISettingsService settings)
        {

            string culture = Language_CurrentIndex == 0 // same as system
                                 ? App.AllowedCultures.Contains(
                                       CultureInfo.CurrentCulture.Name, StringComparer.OrdinalIgnoreCase
                                   )                                     // same as system is allowed
                                       ? CultureInfo.CurrentCulture.Name // same as system
                                       : App.AllowedCultures[1]          // en-US
                                 : App.AllowedCultures[Language_CurrentIndex];

            Resources.Culture = new(culture); // auto updates UI
            CultureInfo.CurrentCulture = Resources.Culture;

            settings.Set("Language.Culture", culture);

        }

        private void RunThemeChangeProtocol(ISettingsService settings)
        {

            settings.Set("GUI.FollowSystem", GUI_CustomTheme ? "0" : "1");
            settings.Set("GUI.DarkTheme", GUI_CustomTheme ? "1" : "0");

            _ = Application.Current?.RequestedThemeVariant = !GUI_CustomTheme
                                                                 ? ThemeVariant.Default
                                                                 : GUI_DarkTheme
                                                                     ? ThemeVariant.Dark
                                                                     : ThemeVariant.Light;

        }

        [RelayCommand]
        private void SaveSettings()
        {

            var settings = ApplicationServices.Get<ISettingsService>();

            RunLanguageChangeProtocol(settings);
            RunThemeChangeProtocol(settings);

            settings.Set("Screenshots.AspectRatio", (int)Screenshots_AspectRatio);
            settings.Set("Screenshots.ColorBlindness", (int)Screenshots_ColorBlindness);
			settings.Set("Screenshots.BlacklistIsWhitelist", Screenshots_BlacklistIsWhitelist ? "1" : "0");

			settings.Save();

        }

    }

}
