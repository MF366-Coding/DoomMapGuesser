/*
 * ________                   ______  ___           _________
 * ___  ___\_______________ _____   |/ _/_____________  ____/__  ________________________
 * __  / /_/ ___\ ___\  __ `___\  /|_/ /  __ `/_  ___\ / ___  / /_/ __\  ___/  ___/  ___/
 * _  /_/ / /_////_/_/ / / / /_/ /  / // /_/ /_  /_////_/ // /_/ /  __(__  )(__  )  /
 * /_____/\____\____/_/ /_/ /_/_/  /_/ \__,_/_  .___\____/ \__,_/\___/____//____//_/
 *                                           /_/
 *
 * Copyright (c) 2024-2026 Matthew
 * MIT License
 *
 * DoomMapGuessr - the geo-guessing game of DOOM
 *
 */

using System;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Reflection;
using System.Threading.Tasks;

using Avalonia;

using DoomMapGuessr.Data.Connection;
using DoomMapGuessr.Helpers;
using DoomMapGuessr.Services;
using DoomMapGuessr.Services.Cache;
using DoomMapGuessr.Services.Cache.Abstractions;
using DoomMapGuessr.Services.Settings;
using DoomMapGuessr.ViewModels;

using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;


namespace DoomMapGuessr
{

    internal sealed class Program
    {

        private const string TRUE = "1";
        private const string FALSE = "0";

        private const string DB_URL = "https://raw.githubusercontent.com/MF366-Coding/DoomMapGuessr/refs/heads/main/data/MAPDAT4.db";
        private const string DB_DOLU_URL = "https://raw.githubusercontent.com/MF366-Coding/DoomMapGuessr/refs/heads/main/data/MAPDAT4.dolu";
        private const string CACHED_DB_ENTRYNAME = "__0";

        // DAY_TICKS constant was obtained using C# interactive mode and DateTime
        private const long DAY_TICKS = 864000000000;
        private const long WEEK_TICKS = DAY_TICKS * 7;
        private const long MONTH_TICKS = DAY_TICKS * 30; // ticks in a 30-day month
        private const long TRIMESTER_TICKS = DAY_TICKS * 90; // ticks in a trimester where every month has 30 days
        private const long SEMESTER_TICKS = DAY_TICKS * 180; // ticks in a semester where every month has 30 days
        private const long YEAR_TICKS = DAY_TICKS * 365; // ignoring leap years cuz physics says so :)

        public static IHost Host { get; private set; } = null!;

        public static string AppDataDirectory =>
            Path.Join(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "dev.mf366.doommapguessr");

        // Avalonia configuration, don't remove; also used by visual designer.
        public static AppBuilder BuildAvaloniaApp() =>
            AppBuilder.Configure<App>()
                      .UsePlatformDetect()
                      .WithInterFont()
                      .LogToTrace();

        public static IHostBuilder CreateHostBuilder(
            string[] args
        ) =>
            Microsoft.Extensions.Hosting.Host.CreateDefaultBuilder(args)
                     .ConfigureServices((
                                            ctx,
                                            services
                                        ) =>
                                        {

                                            services.AddSingleton<ISettingsService>(_ => new IniSettingsService(
                                                                                        Path.Join(AppDataDirectory, "config.ini")
                                                                                    )
                                            );

                                            services.AddSingleton<IFullCachingService>(_ => new CachingService(Path.Join(AppDataDirectory, "AppCache")));

                                            services.AddSingleton<MainWindowViewModel>();
                                            services.AddSingleton<HomePageViewModel>();
                                            services.AddSingleton<ClassicModeViewModel>();
                                            services.AddSingleton<PrecisionModeViewModel>();
                                            services.AddSingleton<AchievementsUnlockablesViewModel>();
                                            services.AddSingleton<SettingsPageViewModel>();

                                            services.AddSingleton<SqLiteConnectionFactory>();

                                            // MainWindowViewModel is both the view model and the navigation service
                                            services.AddSingleton<INavigationService>(s => s.GetRequiredService<MainWindowViewModel>());

                                        }
                     );

        private static void PrepareApplicationSettingsInternally(ISettingsService settings)
        {

            #region Language Settings

            if (!settings.Contains("Language.?"))
                settings.Set<string?>("Language.*", null);

            if (!settings.Contains("Language.Culture") ||
                !CultureInfo.GetCultures(CultureTypes.AllCultures)
                    .Any(
                        c => String.Equals(settings.GetString("Language.Culture"),
                            c.Name,
                            StringComparison.OrdinalIgnoreCase)
                    )
                )
            {

                settings.Set(
                    "Language.Culture", App.AllowedCultures.Contains(App.SystemCulture.Name, StringComparer.OrdinalIgnoreCase)
                                            ? App.SystemCulture.Name
                                            : App.AllowedCultures[0]
                );

            }

            #endregion

            #region GUI Settings

            if (!settings.Contains("GUI.?"))
                settings.Set<string?>("GUI.*", null);

            string? followSystem = settings.GetString("GUI.FollowSystem");

            if (!settings.Contains("GUI.FollowSystem") || (followSystem != FALSE && followSystem != TRUE))
                settings.Set("GUI.FollowSystem", 1);

            string? darkTheme = settings.GetString("GUI.DarkTheme");

            if (!settings.Contains("GUI.DarkTheme") || (darkTheme != FALSE && darkTheme != TRUE))
                settings.Set("GUI.DarkTheme", 1);

            #endregion

            #region Database Settings

            if (!settings.Contains("Database.?"))
                settings.Set<string?>("Database.*", null);

            int periodicity = settings.GetInt32("Database.CheckPeriodicityMode");

            if (!settings.Contains("Database.CheckPeriodicityMode") || periodicity < 1 || periodicity > 8)
                settings.Set("Database.CheckPeriodicityMode", 3); // check weekly

            if (!settings.Contains("Database.DateOfLastCheck") || settings.GetInt64("Database.DateOfLastCheck") == -1)
                settings.Set("Database.DateOfLastCheck", new DateTime(0).Ticks.ToString());

            #endregion

            #region Screenshot Settings

            if (!settings.Contains("Screenshots.?"))
                settings.Set<string?>("Screenshots.*", null);

            int aspectRatio = settings.GetInt32("Screenshots.AspectRatio");

            if (!settings.Contains("Screenshots.AspectRatio") || aspectRatio < 0 || aspectRatio > 3)
                settings.Set("Screenshots.AspectRatio", 0);

            int colorBlindness = settings.GetInt32("Screenshots.ColorBlindness");

            if (!settings.Contains("Screenshots.ColorBlindness") || colorBlindness < 0 || colorBlindness > 4)
                settings.Set("Screenshots.ColorBlindness", 0);

            #endregion

            #region Update Settings

            if (!settings.Contains("Update.?"))
                settings.Set<string?>("Update.*", null);

            string? checkUpd = settings.GetString("Update.Check");

            if (!settings.Contains("Update.Check") || (checkUpd != TRUE && checkUpd != FALSE))
                settings.Set("Update.Check", 1); // 1 for always check, 0 for never check

            #endregion

        }

        public static void PrepareApplicationSettings(
            ISettingsService settings
        )
        {

            if (settings is IniSettingsService { IsIniParsed: false } ini)
                ini.Load().Parse();

            PrepareApplicationSettingsInternally(settings);

            settings.Save();

        }

        private static async Task PrepareApplicationSettingsAsync(
            ISettingsService settings
        )
        {

            if (settings is IniSettingsService { IsIniParsed: false } ini)
                ini.Load().Parse();

            PrepareApplicationSettingsInternally(settings);

            await settings.SaveAsync();

        }

        private static async Task<DatabaseFetchResult> DownloadSqliteDatabase_CheckPeriodicallyAsync(string? dbSourceOverride, string? doluSourceOverride, bool cacheExists, long dateOfLastCheck, long tickDifference)
        {

            var settings = ApplicationServices.Get<ISettingsService>();
            var cache = ApplicationServices.Get<IFullCachingService>();

            try
            {

                string doluSource = doluSourceOverride ?? DB_DOLU_URL;
                string doluString = (await DatabaseFetcher.FetchStringAsync(doluSource, default)).Trim();
                long dateOfLastDatabaseUpdate = Int64.Parse(doluString);

                if ((dateOfLastDatabaseUpdate - dateOfLastCheck) < tickDifference && cacheExists)
                    throw new DummyException("Use cached database instead");

                string dbSource = dbSourceOverride ?? DB_URL;
                byte[] databaseBytes = await DatabaseFetcher.FetchBytesAsync(dbSource, default);
                await cache.SetAsync(CACHED_DB_ENTRYNAME, databaseBytes, CacheTarget.Persistent);
				settings.Set("Database.DateOfLastCheck", DateTime.Now.Ticks);

                await settings.SaveAsync();

			}
            catch (Exception ex) when (ex is HttpRequestException or OverflowException or FormatException or DummyException)
            {

				settings.Set("Database.DateOfLastCheck", DateTime.Now.Ticks);

                await settings.SaveAsync();

				if (await cache.GetBytesAsync(CACHED_DB_ENTRYNAME) is null)
                    return DatabaseFetchResult.CheckErrorNoCache; // critical error

            }
			
			return DatabaseFetchResult.CheckAndCache;

        }


        public static async Task<DatabaseFetchResult> DownloadSqliteDatabaseAsync(string? dbSourceOverride = null, string? doluSourceOverride = null)
        {

            var settings = ApplicationServices.Get<ISettingsService>();
            var cache = ApplicationServices.Get<IFullCachingService>();

            long dateOfLastCheck = settings.GetInt64("Database.DateOfLastCheck");
            bool databaseCacheExists = cache.Exists(CACHED_DB_ENTRYNAME);

            if (dateOfLastCheck < 1)
            {

                // will always try to cache if it's the first time playing
                // ticks = 0 is not guaranteed to mean that it's the first time playing
                // but it's a good aproximation
                // also who the fuck playing DoomMapGuessr in the big 0001 :sob:
                return await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, 1);

            }

            return ApplicationServices.Get<ISettingsService>().GetInt32("Database.CheckPeriodicityMode") switch
            {

                2 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, DAY_TICKS),
                3 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, WEEK_TICKS),
                4 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, MONTH_TICKS),
                5 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, TRIMESTER_TICKS),
                6 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, SEMESTER_TICKS),
                7 => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, YEAR_TICKS),

                8 when databaseCacheExists is false => DatabaseFetchResult.CheckErrorNoCache, // in this case, not an error, but still falls into the same category 

                // this is case 1 (previously case 2) which is the default
                _ => await DownloadSqliteDatabase_CheckPeriodicallyAsync(dbSourceOverride, doluSourceOverride, databaseCacheExists, dateOfLastCheck, 1) // at least 1 tick of difference

            };

        }

        /// <summary>
        /// DoomMapGuessr entry point.
        /// </summary>
        /// <param name="args">Commandline arguments</param>
        /// <remarks>
        /// Initialization code. Don't use any Avalonia, third-party APIs or any
        /// SynchronizationContext-reliant code before AppMain is called: things aren't initialized
        /// yet and stuff might break.
        /// </remarks>
        [STAThread]
        public static async Task<int> Main(
            string[] args
        )
        {

            // DoomMapGuessr [DbZeroSource] [DoluZeroSource]
            await PrepareRequirementsAsync(args);

            BuildAvaloniaApp()
#if DEBUG
                .WithDeveloperTools()
#endif
                .StartWithClassicDesktopLifetime(args);

            return 0;

        }

        private static void PrepareDependencyInjection(string[] args)
        {

            Host = CreateHostBuilder(args).Build();
            Host.Start();
            ApplicationServices.Root = Host.Services;

        }

        private static async Task PrepareDependencyInjectionAsync(string[] args)
        {

            Host = CreateHostBuilder(args).Build();
            await Host.StartAsync();
            ApplicationServices.Root = Host.Services;

        }

        public static void PrepareRequirements(string[] args)
        {

            // Host and DI
            PrepareDependencyInjection(args);
            ApplicationServices.VersionInfo = new(Assembly.GetExecutingAssembly());

            PrepareApplicationSettings(ApplicationServices.Get<ISettingsService>());

            // Fetch latest release
            if (ApplicationServices.Get<ISettingsService>().GetBoolean("Update.Check"))
                ApplicationServices.SavedRelease = ReleaseFetcher.FetchLatest("mf366-dev", "DoomMapGuessr");

            DownloadSqliteDatabase();

        }

        // TODO: implement this method (see DownloadSqliteDatabaseAsync in this file)
        // XXX: very important: we are not throwing NotImplemented solely cuz it breaks design mode
        // XXX: THIS HAS TO BE CHANGED LATER
        private static void DownloadSqliteDatabase() { }

        public static async Task PrepareRequirementsAsync(string[] args)
        {

            // Host and DI
            await PrepareDependencyInjectionAsync(args);
            ApplicationServices.VersionInfo = new(Assembly.GetExecutingAssembly());

            await PrepareApplicationSettingsAsync(ApplicationServices.Get<ISettingsService>());

            // Fetch latest release
            if (ApplicationServices.Get<ISettingsService>().GetBoolean("Update.Check"))
                ApplicationServices.SavedRelease = await ReleaseFetcher.FetchLatestAsync("mf366-dev", "DoomMapGuessr");

#if DEBUG
            bool argsExist = args.Length >= 2;
            await DownloadSqliteDatabaseAsync(argsExist ? args[0] : DB_URL, args.Length != 0 ? args[1] : DB_DOLU_URL);
#else
            await DownloadSqliteDatabaseAsync();
#endif

        }

    }

}
