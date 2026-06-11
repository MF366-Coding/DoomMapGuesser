using System;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.IO;
using System.Threading.Tasks;

using IniParser.Model;
using IniParser.Model.Configuration;
using IniParser.Model.Formatting;
using IniParser.Parser;


namespace DoomMapGuessr.Services.Settings
{

    /// <summary>
    /// A service that handles storage of settings in INI format.
    /// </summary>
    /// <remarks>
    /// Initializes this service with a path to the settings file.
    /// </remarks>
    /// <param name="filepath">The filepath</param>
    public sealed class IniSettingsService(
        string filepath
    ) : ISettingsService,
        IDisposable,
        IAsyncDisposable
    {

        private readonly IniParserConfiguration defaultConfiguration = new()
        {

            AllowCreateSectionsOnFly = true,
            AllowDuplicateKeys = false,
            AllowDuplicateSections = false,
            AllowKeysWithoutSection = false,
            AssigmentSpacer = " ",
            CaseInsensitive = true,
            CommentString = ";",
            ConcatenateDuplicateKeys = true,
            KeyValueAssigmentChar = '=',
            NewLineStr = Environment.NewLine,
            OverrideDuplicateKeys = false,
            SectionEndChar = ']',
            SectionStartChar = '[',
            ThrowExceptionsOnError = true

        };

        private readonly string pathToSettings = filepath;

        private IniData? actualIni;

        private bool disposedValue;

        private string stringifiedData = "";

        /// <summary>
        /// Initializes this service with a representation of the settings file.
        /// </summary>
        /// <param name="file">The file</param>
        public IniSettingsService(
            FileInfo file
        ) : this(file.FullName) { }

        /// <summary>
        /// Whether the data has been loaded and parsed.
        /// </summary>
        [MemberNotNullWhen(true, nameof(actualIni))]
        public bool IsIniParsed => actualIni is not null;

        /// <inheritdoc />
        public async ValueTask DisposeAsync()
        {

            if (!disposedValue)
            {

                await SaveAsync();

                actualIni = null;
                stringifiedData = String.Empty;

                disposedValue = true;

            }

            GC.SuppressFinalize(this);

            await ValueTask.CompletedTask;

        }

        /// <inheritdoc />
        public void Dispose()
        {

            if (!disposedValue)
            {

                Save();

                actualIni = null;
                stringifiedData = String.Empty;

                disposedValue = true;

            }

            GC.SuppressFinalize(this);

        }

        /// <inheritdoc />
        public void Add<T>(
            string key,
            T value
        )
        {

            EnsureIniParsed();

            string[] longFormKey = key.Split('.', 2);

            if (longFormKey.Length < 2)
                throw new ArgumentException("The key must be in a <section>.<key> format", nameof(key));

            actualIni[longFormKey[0]][longFormKey[1]] = value?.ToString() ?? "null";

        }

        /// <inheritdoc />
        public bool Contains(
            string key
        )
        {

            EnsureIniParsed();
            string[] split = key.Split('.', 2);

            return split.Length < 2
                       ? throw new InvalidOperationException(
                             "Key must in format <section>.<key>. If instead you wish to check if a section exists, use <section>.?"
                         )
                       : split[1] == "?"
                           ? // -> ? means "any key" btw in this context
                           actualIni.Sections.ContainsSection(split[0])
                           : actualIni.TryGetKey(key, out _);

        }

        /// <summary>
        /// Not supported for INI.
        /// </summary>
        /// <exception cref="InvalidOperationException"></exception>
        [EditorBrowsable(EditorBrowsableState.Never)]
        public T Get<T>(
            string key,
            T defaultValue = default!
        ) =>
            throw new InvalidOperationException("Cannot Get<T>() for INI. Try GetString() instead.");

        /// <inheritdoc />
        public bool GetBoolean(
            string key
        )
        {

            string? str = GetString(key);

            if (String.IsNullOrEmpty(str))
                return false;

            if (Boolean.TryParse(str, out bool b))
                return b;

            if (Double.TryParse(str, out double d) && Math.Abs(Math.Abs(d) - 1.0) < 0.01)
                return true;

            return Int32.TryParse(str, out int i) && Math.Abs(i) != 0;

        }

        /// <inheritdoc />
        public double GetDouble(
            string key
        ) =>
            Double.TryParse(GetString(key), out double result)
                ? result
                : Double.NaN;

        /// <inheritdoc />
        public int GetInt32(
            string key
        ) =>
            Int32.TryParse(GetString(key), out int result)
                ? result
                : -1;

        /// <inheritdoc />
        public long GetInt64(
            string key
        ) =>
            Int64.TryParse(GetString(key), out long result)
                ? result
                : -1;

        /// <inheritdoc />
        public string GetString(
            string key
        )
        {

            EnsureIniParsed();

            return actualIni.TryGetKey(key, out string? value)
                       ? value
                       : String.Empty;

        }

        /// <inheritdoc />
        public void Save()
        {

            EnsureIniParsed();

            string? contents = actualIni.ToString(new DefaultIniDataFormatter(defaultConfiguration));

            File.WriteAllText(pathToSettings, contents);

        }

        /// <inheritdoc />
        public async Task SaveAsync()
        {

            EnsureIniParsed();

            string? contents = actualIni.ToString(new DefaultIniDataFormatter(defaultConfiguration));

            await File.WriteAllTextAsync(pathToSettings, contents);

        }

        /// <inheritdoc />
        public void Set<T>(
            string key,
            T value
        )
        {

            EnsureIniParsed();
            string[] split = key.Split('.', 2);

            if (split.Length < 2)
            {
                throw new InvalidOperationException(
                    "Key must be in format <section>.<key>. If you wish to instead create a section, use <section>.*"
                );
            }

            if (split[1] == "*")                         // in here we use * cuz it means ALL
                actualIni.Sections.AddSection(split[0]); // value is ignored

            else
                actualIni[split[0]][split[1]] = value is null ? "null" : value.ToString();

        }

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public bool TryGet<T>(
            string key,
            out T value
        ) =>
            throw new InvalidOperationException("TryGet<T> is not supported for INI. Use GetString instead.");

        // ReSharper disable once EmptyDestructor
        /// <summary>
        /// <c>~IniSettingsService</c>
        /// </summary>
        [EditorBrowsable(EditorBrowsableState.Never)]
        ~IniSettingsService() { }

        /// <summary>
        /// Gets a copy of the actual INI data.
        /// </summary>
        /// <returns>The copy</returns>
        public IniData GetCopy()
        {

            EnsureIniParsed();

            return new(actualIni);

        }

        /// <summary>
        /// Loads the settings as a string.
        /// </summary>
        /// <returns>Self</returns>
        public IniSettingsService Load() => Load("; This file was created by DoomMapGuessr.Services.IniSettingsService");

        /// <summary>
        /// Loads the settings as a string.
        /// </summary>
        /// <param name="defaultData">The data to use if the file is missing</param>
        /// <returns>Self</returns>
        public IniSettingsService Load(
            string defaultData
        )
        {

            string? directoryPath = Path.GetDirectoryName(pathToSettings);

            if (!File.Exists(pathToSettings) && directoryPath is not null)
            {

                Directory.CreateDirectory(directoryPath);
                File.WriteAllText(pathToSettings, defaultData);

            }

            stringifiedData = File.ReadAllText(pathToSettings);

            return this;

        }

        /// <summary>
        /// Parses the settings and converts them to actual INI,
        /// using the default parser configuration.
        /// </summary>
        /// <returns>Self</returns>
        public IniSettingsService Parse() => Parse(defaultConfiguration);

        /// <summary>
        /// Parses the settings and converts them to actual INI.
        /// </summary>
        /// <param name="configuration">The parser configuration</param>
        /// <returns>Self</returns>
        public IniSettingsService Parse(
            IniParserConfiguration configuration
        )
        {

            configuration.ThrowExceptionsOnError = true; // force this to be true
            IniDataParser parser = new(configuration);

            actualIni = parser.Parse(stringifiedData);

            return this;

        }

        [MemberNotNull(nameof(actualIni))]
        private void EnsureIniParsed()
        {

            if (!IsIniParsed)
                throw new InvalidDataException("The settings have not been parsed yet");

        }

    }

}
