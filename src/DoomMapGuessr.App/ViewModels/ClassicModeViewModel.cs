using System;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

using Octokit;


namespace DoomMapGuessr.ViewModels
{

    /// <summary>
    /// View model for the classic mode page.
    /// </summary>
    public partial class ClassicModeViewModel : ViewModelBase
    {

        /// <summary>
        /// Initializes the view model.
        /// </summary>
        public ClassicModeViewModel() { }

        [ObservableProperty]
        public partial bool IsGuessingPaneOpen { get; set; } = true;

        [ObservableProperty]
        public partial int UserInput_SecretCount { get; set; } = 0;

        [ObservableProperty]
        public partial int ContentBlurRadius { get; set; } = 5;

        [ObservableProperty]
        public partial string SecretSetterHeading { get; set; } = "0 Secrets";

        [RelayCommand]
        private void ChangeInputSecretCountBy(object? value)
        {

            if (Int32.TryParse(value as string, out int result))
                UserInput_SecretCount += result;

        }

        public void UpdateSecretSetterHeading() => SecretSetterHeading = $"{UserInput_SecretCount} Secrets";

        // todo: handle the classic mode
        [RelayCommand]
        private void ToggleGuessingPane()
        {

            IsGuessingPaneOpen = !IsGuessingPaneOpen;
            ContentBlurRadius = IsGuessingPaneOpen ? 5 : 0;

        }

    }

}
