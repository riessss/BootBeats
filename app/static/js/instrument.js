const instrumentBtn = document.getElementById("instrumentBtn");
const dropupMenu = document.getElementById("dropupMenu");
const dropupMenuList = document.getElementById("dropupMenuList"); // the <ul> inside dropupMenu
const instrumentList = document.getElementById("instrumentList");

// Open instrument menu
instrumentBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  dropupMenu.classList.toggle("hidden");
});

// Close instrument menu
document.addEventListener("click", (e) => {
  if (!dropupMenu.contains(e.target) && !instrumentBtn.contains(e.target)) {
    dropupMenu.classList.add("hidden");
  }
});

// Add instrument to menu
dropupMenuList.addEventListener('click', async (e) => {
  if (e.target && e.target.classList.contains('add-instrument-item')) {
    const instrumentId = e.target.dataset.id;
    const instrumentHtml = e.target.innerHTML;

    try {
      const response = await fetch('/instrument/add_instrument', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song_id: currentSongId, instrument_id: instrumentId })
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      console.log('Response from server:', data);

      if (data.success) {
        const newDiv = document.createElement('div');
        newDiv.classList.add('flex', 'flex-row', 'items-center');
        newDiv.dataset.id = instrumentId;
        newDiv.innerHTML = `
          <div class="flex-shrink-0 bg-white p-4 w-40 h-24 text-center">
            ${instrumentHtml}
            <button type="button" class="text-red-500 hover:text-red-700 font-bold pl-10 remove-instrument-btn">x</button>
          </div>
        `;
        instrumentList.appendChild(newDiv);

        e.target.remove();
        dropupMenu.classList.add('hidden');
      } else {
        alert('Failed to add instrument on server: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      alert('Error adding instrument: ' + error.message);
    }
  }
});

// Delete instrument from list
instrumentList.addEventListener('click', async (e) => {
  if (e.target && e.target.classList.contains('remove-instrument-btn')) {
    const instrumentDiv = e.target.closest('[data-id]');
    const instrumentId = instrumentDiv.dataset.id;

    try {
      const response = await fetch(`/instrument/${currentSongId}/${instrumentId}`, {
        method: 'DELETE'
      });

      const data = await response.json();
      console.log('Delete response:', data);

      if (response.ok && data.success) {
        instrumentDiv.remove();
      } else {
        alert('Failed to delete instrument: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      alert('Error deleting instrument: ' + error.message);
    }
  }
});

