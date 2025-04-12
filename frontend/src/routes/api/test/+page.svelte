<script>
  import { onMount } from 'svelte';
  import { user } from '$lib/stores';
  
  let results = {
    config: null,
    chats: null,
    tags: null,
    models: null,
    tools: null,
    error: null
  };
  
  let loading = {
    config: false,
    chats: false,
    tags: false,
    models: false,
    tools: false
  };
  
  async function testConfigAPI() {
    loading.config = true;
    try {
      const response = await fetch('/api/config');
      results.config = await response.json();
    } catch (error) {
      results.error = `Config API error: ${error.message}`;
    } finally {
      loading.config = false;
    }
  }
  
  async function testChatsAPI() {
    loading.chats = true;
    try {
      const response = await fetch('/api/chats', {
        headers: {
          Authorization: `Bearer ${localStorage.token}`
        }
      });
      results.chats = await response.json();
    } catch (error) {
      results.error = `Chats API error: ${error.message}`;
    } finally {
      loading.chats = false;
    }
  }
  
  async function testTagsAPI() {
    loading.tags = true;
    try {
      const response = await fetch('/api/chats/tags', {
        headers: {
          Authorization: `Bearer ${localStorage.token}`
        }
      });
      results.tags = await response.json();
    } catch (error) {
      results.error = `Tags API error: ${error.message}`;
    } finally {
      loading.tags = false;
    }
  }
  
  async function testModelsAPI() {
    loading.models = true;
    try {
      const response = await fetch('/api/models', {
        headers: {
          Authorization: `Bearer ${localStorage.token}`
        }
      });
      results.models = await response.json();
    } catch (error) {
      results.error = `Models API error: ${error.message}`;
    } finally {
      loading.models = false;
    }
  }
  
  async function testToolsAPI() {
    loading.tools = true;
    try {
      const response = await fetch('/api/tools', {
        headers: {
          Authorization: `Bearer ${localStorage.token}`
        }
      });
      results.tools = await response.json();
    } catch (error) {
      results.error = `Tools API error: ${error.message}`;
    } finally {
      loading.tools = false;
    }
  }
  
  onMount(async () => {
    if (!$user) {
      results.error = "User not logged in. Please log in first.";
      return;
    }
    
    // Test all APIs
    await testConfigAPI();
    await testChatsAPI();
    await testTagsAPI();
    await testModelsAPI();
    await testToolsAPI();
  });
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">API Routes Test</h1>
  
  {#if results.error}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p>{results.error}</p>
    </div>
  {/if}
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <!-- Config API -->
    <div class="border rounded p-4">
      <h2 class="text-xl font-semibold mb-2">Config API</h2>
      {#if loading.config}
        <p>Loading...</p>
      {:else if results.config}
        <pre class="bg-gray-100 p-2 rounded overflow-auto max-h-60">{JSON.stringify(results.config, null, 2)}</pre>
      {:else}
        <p>No data</p>
      {/if}
      <button 
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        on:click={testConfigAPI}
      >
        Test Config API
      </button>
    </div>
    
    <!-- Chats API -->
    <div class="border rounded p-4">
      <h2 class="text-xl font-semibold mb-2">Chats API</h2>
      {#if loading.chats}
        <p>Loading...</p>
      {:else if results.chats}
        <pre class="bg-gray-100 p-2 rounded overflow-auto max-h-60">{JSON.stringify(results.chats, null, 2)}</pre>
      {:else}
        <p>No data</p>
      {/if}
      <button 
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        on:click={testChatsAPI}
      >
        Test Chats API
      </button>
    </div>
    
    <!-- Tags API -->
    <div class="border rounded p-4">
      <h2 class="text-xl font-semibold mb-2">Tags API</h2>
      {#if loading.tags}
        <p>Loading...</p>
      {:else if results.tags}
        <pre class="bg-gray-100 p-2 rounded overflow-auto max-h-60">{JSON.stringify(results.tags, null, 2)}</pre>
      {:else}
        <p>No data</p>
      {/if}
      <button 
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        on:click={testTagsAPI}
      >
        Test Tags API
      </button>
    </div>
    
    <!-- Models API -->
    <div class="border rounded p-4">
      <h2 class="text-xl font-semibold mb-2">Models API</h2>
      {#if loading.models}
        <p>Loading...</p>
      {:else if results.models}
        <pre class="bg-gray-100 p-2 rounded overflow-auto max-h-60">{JSON.stringify(results.models, null, 2)}</pre>
      {:else}
        <p>No data</p>
      {/if}
      <button 
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        on:click={testModelsAPI}
      >
        Test Models API
      </button>
    </div>
    
    <!-- Tools API -->
    <div class="border rounded p-4">
      <h2 class="text-xl font-semibold mb-2">Tools API</h2>
      {#if loading.tools}
        <p>Loading...</p>
      {:else if results.tools}
        <pre class="bg-gray-100 p-2 rounded overflow-auto max-h-60">{JSON.stringify(results.tools, null, 2)}</pre>
      {:else}
        <p>No data</p>
      {/if}
      <button 
        class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        on:click={testToolsAPI}
      >
        Test Tools API
      </button>
    </div>
  </div>
</div>
