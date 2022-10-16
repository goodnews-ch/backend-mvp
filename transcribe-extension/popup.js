document.getElementById('parent').addEventListener('click', async () => {
  clicked = true
  const tab = await getCurrentTab()
  if(!tab) return alert('Require an active tab')
  await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['main.js']
  })
  document.getElementById('parent').removeChild(document.getElementById('start'))
})

async function getCurrentTab() {
  const queryOptions = { active: true, lastFocusedWindow: true }
  const [tab] = await chrome.tabs.query(queryOptions)
  return tab
}

function getText(){
  return document.body.innerText
}

chrome.runtime.onMessage.addListener(({ message }) => {
  if(message == 'transcriptavailable') {
      showLatestTranscript()
  }
})

function showLatestTranscript() {
  chrome.storage.local.get('transcript', ({ transcript }) => {
      document.getElementById('transcript').innerHTML = transcript
  })
}