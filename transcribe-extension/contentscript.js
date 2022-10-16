console.log("Content script?!")

async function getCurrentTab() {
    const queryOptions = { active: true, lastFocusedWindow: true }
    const [tab] = await chrome.tabs.query(queryOptions)
    return tab
  }

window.addEventListener('load', function load(event) {
    console.log("Hello!")
    var iframe = document.createElement('iframe');
    /* some settings, these are mine */
    iframe.style.width = "250px";
    iframe.style.background = "#eee";
    iframe.style.height = "420px";
    iframe.style.position = "fixed";
    iframe.style.top = "0px";
    iframe.style.right = "0px";
    iframe.style.zIndex = "1000000000000000";
    iframe.style.opacity = "100%";
    iframe.frameBorder = "none";
    /* end of settings */
    iframe.src = chrome.runtime.getURL("popup.html");
    document.body.appendChild(iframe);
  });