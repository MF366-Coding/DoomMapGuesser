using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using DoomMapGuessr.Services.Settings;


namespace DoomMapGuessr.ViewModels;

/// <summary>
/// View model for the classic mode page.
/// </summary>
public partial class ClassicModeViewModel : ViewModelBase
{
	/// <summary>
	/// Initializes the view model.
	/// </summary>
	public ClassicModeViewModel() => ApplicationServices.Get<ISettingsService>().SettingsChanged += OnBlurEffectSettingChanged;
	
	private int blurRadius = 5;

	private void OnBlurEffectSettingChanged(SettingsChangedEventArgs<object?> args)
	{
		if (args.Key != "GUI.BlurEffects" || args.NewValue is not string newValue || (newValue != "1" && newValue != "0"))
			return;

		blurRadius = newValue == "1" ? 5 : 0;
	}

	[ObservableProperty]
	public partial bool IsGuessingPaneOpen { get; set; } = true;

	[ObservableProperty]
	public partial int UserInput_SecretCount { get; set; } = 0;

	[ObservableProperty]
	public partial int ContentBlurRadius { get; set; } = 0;

	// todo: handle the classic mode
	[RelayCommand]
	private void ToggleGuessingPane()
	{
		IsGuessingPaneOpen = !IsGuessingPaneOpen;
		ContentBlurRadius = IsGuessingPaneOpen ? blurRadius : 0;
	}

	/// <summary>
	/// Unsubscribes from the <c>SettingsChanged</c> event to avoid resource leaks.
	/// </summary>
	/// <remarks>
	/// Called when <see cref="ClassicModeViewModel"/> is destroyed.
	/// </remarks>
	~ClassicModeViewModel()
	{
		ApplicationServices.Get<ISettingsService>().SettingsChanged -= OnBlurEffectSettingChanged;
	}

	[RelayCommand]
	private void SubmitGuess()
	{
		// todo: code submitting logic
	}

	[RelayCommand]
	private void GiveUp()
	{
		// todo: code giving up logic
	}
}
