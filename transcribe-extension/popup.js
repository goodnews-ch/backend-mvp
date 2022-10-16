document.getElementById('start').addEventListener('click', async () => {
  const tab = await getCurrentTab()
  if(!tab) return alert('Require an active tab')
  chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['main.js']
  })
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

chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  console.log('hi')
  if (changeInfo.status == 'complete') {
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
      let url = tabs[0].url;
      // use `url` here inside the callback because it's asynchronous!
      document.getElementById('transcript').innerHTML = url
      
  })  
  }
})