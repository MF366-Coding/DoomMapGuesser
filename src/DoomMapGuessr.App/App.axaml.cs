using System.Globalization;
using System.Linq;

using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Data.Core.Plugins;
using Avalonia.Markup.Xaml;
using Avalonia.Styling;

using DoomMapGuessr.Services.Settings;
using DoomMapGuessr.ViewModels;
using DoomMapGuessr.Views;


namespace DoomMapGuessr
{

    /// <summary>
    /// Avalonia app.
    /// Contains Avalonia-specific functionality.
    /// </summary>
    public class App : Application
    {

        /// <summary>
        /// Allowed cultures. First item is a filler - do not use.
        /// </summary>
        public static string[] AllowedCultures { get; } = ["", "en-US", "pt-br", "pt-PT"];

        /// <summary>
        /// System culture.
        /// </summary>
        public static CultureInfo SystemCulture => CultureInfo.InstalledUICulture;

        /// <remarks>
        /// Avalonia function. Do not mess with.
        /// </remarks>
        private static void DisableAvaloniaDataAnnotationValidation()
        {

            // plugins to remove
            var dataValidationPluginsToRemove = BindingPlugins.DataValidators.OfType<DataAnnotationsValidationPlugin>().ToArray();

            // remove each entry found
            foreach (var plugin in dataValidationPluginsToRemove)
                _ = BindingPlugins.DataValidators.Remove(plugin);

        }

        /// <inheritdoc />
        public override void Initialize() => AvaloniaXamlLoader.Load(this);

        /// <summary>
        /// Runs after Avalonia is initialized.
        /// </summary>
        public override void OnFrameworkInitializationCompleted()
        {

            #region Design Mode Setup

            if (Design.IsDesignMode)
                Program.PrepareRequirements([]);

            #endregion

            // Theme
            RequestedThemeVariant = ApplicationServices.Get<ISettingsService>().GetBoolean("GUI.FollowSystem")
                                        ? ThemeVariant.Default
                                        : ApplicationServices.Get<ISettingsService>().GetBoolean("GUI.DarkTheme")
                                            ? ThemeVariant.Dark
                                            : ThemeVariant.Light;

            // Language
            Strings.Resources.Culture = new(ApplicationServices.Get<ISettingsService>().GetString("Language.Culture") ?? "en-US");
            CultureInfo.CurrentCulture = Strings.Resources.Culture;

            // Desktop setup
            if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            {

                // ReSharper disable CommentTypo
                // Avoid duplicate validations from both Avalonia and the CommunityToolkit.
                // More info: https://docs.avaloniaui.net/docs/guides/development-guides/data-validation#manage-validationplugins
                // ReSharper restore CommentTypo
                DisableAvaloniaDataAnnotationValidation();

                desktop.MainWindow = new MainWindow
                {
                    DataContext = ApplicationServices.Get<MainWindowViewModel>()
                };

            }

            base.OnFrameworkInitializationCompleted();

        }

    }

}
