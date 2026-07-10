using System.Diagnostics;
using System.Threading.Tasks;


namespace DoomMapGuessr.Helpers;


    /// <summary>
    /// Helper class for default webbrowser usage.
    /// </summary>
    public static class WebBrowser
    {

        /// <summary>
        /// Opens a URL in the default browser.
        /// </summary>
        /// <param name="url">The URL</param>
        /// <returns><c>true</c> if successful</returns>
        public static bool OpenUrl(
            string url
        )
        {

            try
            {
                ProcessStartInfo psi = new()
                {

                    FileName = url,
                    UseShellExecute = true

                };

                using Process? _ = Process.Start(psi);

                return true;
            }
            catch
            {
                return false;
            }

        }

        /// <summary>
        /// Opens a URL in the default browser, async.
        /// </summary>
        /// <param name="url">The URL to open</param>
        /// <returns></returns>
        public static async Task<Process?> OpenUrlAsync(
            string url
        )
        {

            try
            {
                ProcessStartInfo psi = new()
                {

                    FileName = url,
                    UseShellExecute = true

                };

                return await Task.Run(() => Process.Start(psi));
            }
            catch
            {
                return null;
            }

        }

    }
