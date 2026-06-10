using Avalonia.Controls;
using Avalonia.Input;

using DoomMapGuessr.ViewModels;


namespace DoomMapGuessr.Views
{

    /// <summary>
    /// Page for playing DoomMapGuessr Classic Mode.
    /// </summary>
    public partial class ClassicModePage : UserControl
    {

        /// <summary>
        /// Initializes the page.
        /// </summary>
        public ClassicModePage() => InitializeComponent();

        private bool isOutsidePane = true;

        private void OnPointerEnteredPane(object? sender, Avalonia.Input.PointerEventArgs e)
        {

            if (DataContext is not ClassicModeViewModel vm)
                return;

            if (isOutsidePane && !vm.IsGuessingPaneOpen)
                vm.ToggleGuessingPaneCommand.Execute(null);

            isOutsidePane = false;

        }

        private void OnPointerExitedPane(object? sender, Avalonia.Input.PointerEventArgs e) => isOutsidePane = true;

    }

}
