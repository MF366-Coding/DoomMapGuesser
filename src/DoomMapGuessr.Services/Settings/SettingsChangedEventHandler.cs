namespace DoomMapGuessr.Services.Settings;


/// <summary>
/// Handler for events triggered by edits to the settings.
/// </summary>
/// <typeparam name="T">The value type</typeparam>
/// <param name="eventArgs">The event's arguments</param>
public delegate void SettingsChangedEventHandler<T>(SettingsChangedEventArgs<T> eventArgs);
