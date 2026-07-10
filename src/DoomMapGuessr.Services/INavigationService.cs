namespace DoomMapGuessr.Services;


    // todo: this should be an actual service
    // meaning MainWindowViewModel should not have
    // full control over this shit

    /// <summary>
    /// A navigation service.
    /// </summary>
    public interface INavigationService
    {

        /// <summary>
        /// Navigates to a page.
        /// </summary>
        /// <param name="pageName">The name of the page.</param>
        void NavigateTo(
            string pageName
        );

        /// <summary>
        /// Navigates to a page with some parameters.
        /// </summary>
        /// <param name="pageName">The name of the page</param>
        /// <param name="parameter">A parameter to be passed</param>
        void NavigateTo(
            string pageName,
            object? parameter
        );

    }
