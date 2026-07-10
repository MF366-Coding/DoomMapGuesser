namespace DoomMapGuessr.Services.Cache.Abstractions;


    /// <summary>
    /// A caching service made of asynchronous and synchronous components.
    /// </summary>
    public interface IFullCachingService : ICachingService,
                                           ICachingServiceAsync;
