document.addEventListener('DOMContentLoaded', () => {
  const loadingEl = document.getElementById('loading-screen');
  const mainEl = document.getElementById('main-content');
  const form = document.querySelector('form');
  const totalCountElement = document.querySelector('.total-entries');
  const tableBody = document.querySelector('tbody');
  let initialLoadComplete = false;
  let lastHiddenTime = 0;

  const hideLoadingScreen = () => {
    loadingEl?.style.setProperty('display', 'none');
    mainEl?.style.setProperty('display', 'block');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const fullUrl = document.querySelector('[name="fullUrl"]').value.trim();
    const shortUrl =
      document.querySelector('[name="shortUrl"]').value.trim() || null;

    if (!fullUrl) return alert('Please enter a full URL');

    const response = await fetch('/api/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full: fullUrl, short: shortUrl })
    });

    const data = await response.json();

    if (data?.url) window.location.href = window.location.origin + data.url;
    else if (data?.error) alert(data.error);
  };

  const updateEntries = async () => {
    const response = await fetch('/api/all');

    const data = await response.json();
    if (!Array.isArray(data)) return;

    tableBody.innerHTML = data
      .map(
        ({ full, short, clicks }) => `
        <tr class="border-b bg-[#131214] border-gray-700 hover:bg-gray-600">
          <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            <a id="full" class="text-[#00ffff]" href="${full}">
              ${full.length > 50 ? full.slice(0, 50) + '...' : full}
            </a>
          </th>
          <td class="px-6 py-4">
            <a id="short" href="/${short}/info">${short}</a>
          </td>
          <td class="px-6 py-4">${clicks}</td>
        </tr>
      `
      )
      .join('');

    if (totalCountElement) totalCountElement.textContent = data.length;

    if (!initialLoadComplete) {
      hideLoadingScreen();
      initialLoadComplete = true;
    }
  };

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && Date.now() - lastHiddenTime > 3000) {
      updateEntries();
    }
    if (document.hidden) lastHiddenTime = Date.now();
  });

  if (form) form.addEventListener('submit', handleSubmit);
  updateEntries();
});
