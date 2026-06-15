namespace DoomMapGuessr.Services.Settings
{

	/// <summary>
	/// Arguments to be passed to a <see cref="SettingsChangedEventHandler{T}"/>
	/// when a setting is altered.
	/// </summary>
	/// <typeparam name="T">The value type</typeparam>
	/// <param name="key">See <see cref="Key"/>.</param>
	/// <param name="oldValue">See <see cref="OldValue"/>.</param>
	/// <param name="newValue">See <see cref="NewValue"/>.</param>
	/// <param name="wasOperationSuccessful">See <see cref="WasOperationSuccessful"/>.</param>
	public readonly struct SettingsChangedEventArgs<T>(string key, T oldValue, T newValue, bool wasOperationSuccessful = true)
	{

		/// <summary>
		/// The key whose value was altered.
		/// </summary>
		public string Key { get; init; } = key;

		/// <summary>
		/// The key's old value.
		/// </summary>
		public T OldValue { get; init; } = oldValue;

		/// <summary>
		/// The key's new value.
		/// </summary>
		public T NewValue { get; init; } = newValue;

		/// <summary>
		/// Whether the settings edit operation was successful.
		/// </summary>
		public bool WasOperationSuccessful { get; init; } = wasOperationSuccessful;

	}

}
