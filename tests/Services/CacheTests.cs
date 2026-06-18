#if DEBUG
using System.Diagnostics;

using DoomMapGuessr.Services.Cache;
#endif


namespace DoomMapGuessr.Tests.Services
{

	[TestClass]
	[System.Diagnostics.CodeAnalysis.SuppressMessage("Style", "IDE1006:Naming Styles", Justification = "Refer to OceanApocalypseStudios coding conventions")]

	public class CacheTests
	{

		private static string cacheDirectory = null!;

		private static CachingService CreateService() => new(cacheDirectory);

		private static bool DeleteTestCache()
		{

			try
			{

				Directory.Delete(cacheDirectory, true);
				return true;

			}
			catch (DirectoryNotFoundException)
			{

				return true;

			}
			catch (Exception ex) when (ex is IOException or UnauthorizedAccessException)
			{

#if DEBUG
				Debug.WriteLine("Failed to delete test cache.");
#endif
				return false;

			}

		}

		private static void CreateTestCache()
		{

			try
			{
				Directory.CreateDirectory(cacheDirectory);
			}
			catch (Exception ex) when (ex is IOException or DirectoryNotFoundException or UnauthorizedAccessException)
			{
#if DEBUG
				Debug.WriteLine("Failed to create test cache directory.");
#endif
			}

		}

		[AssemblyInitialize]
		public static void InitialSetup(TestContext testContext)
		{

			cacheDirectory = Path.Join(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "dev.mf366.doommapguessr", "TestCache");
			DeleteTestCache();

			testContext.WriteLine("Initialization complete.");

		}

		[TestMethod]
		public void Cache_Init_CreatesDirectoryIfNonExisting()
		{

			if (!DeleteTestCache())
				Assert.Fail("Cannot test for directory creation if directory already exists.");

			var svc = CreateService();

			Assert.IsTrue(Directory.Exists(cacheDirectory));
			Assert.IsTrue(svc.TemporaryCacheDirectory.Exists);
			Assert.IsTrue(svc.PersistentCacheDirectory.Exists);

		}

		[TestMethod]
		public void Cache_Init_CreatedDirectoryIsRequestedDirectory()
		{

			if (!DeleteTestCache())
				Assert.Fail("Cannot test for directory creation if directory already exists.");

			var svc = CreateService();

			Assert.AreEqual(cacheDirectory, svc.CacheDirectory);
			Assert.IsTrue(Directory.Exists(cacheDirectory));
			Assert.IsTrue(Directory.Exists(svc.CacheDirectory));

		}

		[TestMethod]
		public void Cache_SetMemory_MaintainsInt64Value()
		{

			var svc = CreateService();

			const long value = Int64.MaxValue - 1;

			svc.Set("Cache_SetMemory_MaintainsInt64Value_TestKey", value, CacheTarget.Memory);
			Assert.AreEqual(value, svc.Get<long>("Cache_SetMemory_MaintainsInt64Value_TestKey"));

		}

		[TestMethod]
		public void Cache_SetMemory_MaintainsArrayValue()
		{

			var svc = CreateService();

			svc.Set<string>("Cache_SetMemory_MaintainsStringValue_TestKey", "DoomMapGuessr is very nice", CacheTarget.Memory);
			Assert.AreEqual("DoomMapGuessr is very nice", svc.Get<string>("Cache_SetMemory_MaintainsStringValue_TestKey"));

		}

		[TestMethod]
		public async Task Cache_SetMemoryAsync_MaintainsInt64Value()
		{

			var svc = CreateService();

			const long value = Int64.MaxValue - 1;

			await svc.SetAsync("Cache_SetMemoryAsync_MaintainsInt64Value_TestKey", value, CacheTarget.Memory);
			Assert.AreEqual(value, svc.Get<long>("Cache_SetMemoryAsync_MaintainsInt64Value_TestKey"));

		}

		[TestMethod]
		public async Task Cache_SetMemoryAsync_MaintainsStringValue()
		{

			var svc = CreateService();

			await svc.SetAsync<string>("Cache_SetMemoryAsync_MaintainsStringValue_TestKey", "DoomMapGuessr is very nice", CacheTarget.Memory);
			Assert.AreEqual("DoomMapGuessr is very nice", svc.Get<string>("Cache_SetMemoryAsync_MaintainsStringValue_TestKey"));

		}

		[TestMethod]
		public void Cache_SetMemory_MemoryCanBeOverwritten()
		{

			var svc = CreateService();

			svc.Set("Cache_SetMemory_MemoryCanBeOverwritten_TestKey", "DoomMapGuessr is nice!", CacheTarget.Memory);
			Assert.IsTrue(svc.Get<object>("Cache_SetMemory_MemoryCanBeOverwritten_TestKey") is string oldString && oldString.EndsWith("nice!"));

			svc.Set<string[]>("Cache_SetMemory_MemoryCanBeOverwritten_TestKey", ["Doom", "MapGuessr", "is", "awesome!"], CacheTarget.Memory);
			Assert.IsTrue(svc.Get<object>("Cache_SetMemory_MemoryCanBeOverwritten_TestKey") is string[] newArray && newArray[3] == "awesome!");

		}

		[TestMethod]
		public void Cache_ClearMemory_ClearsMemory()
		{

			var svc = CreateService();

			svc.Set("Cache_ClearMemory_ClearsMemory_TestKey1", "DoomMapGuessr is nice!", CacheTarget.Memory);
			Assert.IsTrue(svc.Get<object>("Cache_ClearMemory_ClearsMemory_TestKey1") is string value && value.EndsWith("nice!"));

			svc.Set("Cache_ClearMemory_ClearsMemory_TestKey2", 30, CacheTarget.Memory);
			Assert.AreEqual(30, svc.Get<int>("Cache_ClearMemory_ClearsMemory_TestKey2"));

			svc.Clear(CacheTarget.Memory);

			Assert.IsNull(svc.Get<object>("Cache_ClearMemory_ClearsMemory_TestKey1"));
			Assert.IsNull(svc.Get<object>("Cache_ClearMemory_ClearsMemory_TestKey2"));

		}

		[TestMethod]
		public void Cache_ClearMemory_DoesNotBlockMemoryUsage()
		{

			var svc = CreateService();

			svc.Set("Cache_ClearMemory_DoesNotBlockMemoryUsage_TestKey1", "DoomMapGuessr is awesome really!", CacheTarget.Memory);
			Assert.IsTrue(svc.Get<object>("Cache_ClearMemory_DoesNotBlockMemoryUsage_TestKey1") is string oldString && oldString.EndsWith("really!"));

			svc.Clear(CacheTarget.Memory);

			svc.Set("Cache_ClearMemory_DoesNotBlockMemoryUsage_TestKey2", "DoomMapGuessr is really awesome!", CacheTarget.Memory);

			Assert.IsNull(svc.Get<object>("Cache_ClearMemory_DoesNotBlockMemoryUsage_TestKey1"));
			Assert.IsTrue(svc.Get<object>("Cache_ClearMemory_DoesNotBlockMemoryUsage_TestKey2") is string newString && newString.EndsWith("awesome!"));

		}

		// todo: add more tests

	}

}
