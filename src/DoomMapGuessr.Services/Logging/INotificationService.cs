using System;


namespace DoomMapGuessr.Services.Logging;


    /// <summary>
    /// A service for notifying the user of certain occurences.
    /// </summary>
    public interface INotificationService
    {

        /// <summary>
        /// Notifies the user of an error.
        /// </summary>
        /// <param name="message">The message</param>
        void NotifyError(
            string message
        );

        /// <summary>
        /// Notifies the user of a critical error (<see cref="Exception" />).
        /// </summary>
        /// <param name="exception">The exception</param>
        /// <param name="context">Additional context or <c>null</c></param>
        void NotifyError(
            Exception exception,
            string? context = null
        );

        /// <summary>
        /// Informs the user of something.
        /// </summary>
        /// <param name="message">The message</param>
        void NotifyInfo(
            string message
        );

        /// <summary>
        /// Warns the user of something.
        /// </summary>
        /// <param name="message">The message</param>
        void NotifyWarning(
            string message
        );

    }
