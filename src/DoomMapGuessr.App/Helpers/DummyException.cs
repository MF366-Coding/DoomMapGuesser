using System;


namespace DoomMapGuessr.Helpers;


    /// <summary>
    /// An exception with the sole purpose of being thrown in
    /// order to force <c>catch</c> statements to run.
    /// </summary>
    internal class DummyException(string message) : Exception(message);
