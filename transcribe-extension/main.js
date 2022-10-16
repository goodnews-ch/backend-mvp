alert('This is an injected script!')
let socket
var send = true
var url 
chrome.storage.local.set({ transcript: '' })

navigator.mediaDevices.getDisplayMedia({ video: true, audio: true }).then(stream => {
    if(stream.getAudioTracks().length == 0) return alert('You must share your tab with audio. Refresh the page.')
    const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })

    socket = new WebSocket('wss://api.deepgram.com/v1/listen?tier=enhanced', ['token', 'fcefb8de1652c7b7444da1d73ff88f642acfc8df'])

    recorder.addEventListener('dataavailable', evt => {
        if(evt.data.size > 0) {
            if (socket.readyState == 1) {
                socket.send(evt.data)
            }
        }
    })

    socket.onopen = () => { recorder.start(1000) }

    socket.onmessage = msg => {
        const { transcript } = JSON.parse(msg.data).channel.alternatives[0]
        console.log('msg received')

        if(transcript) {
            console.log(transcript)
            chrome.storage.local.get('transcript', data => {
                chrome.storage.local.set({
                    transcript: data.transcript += ' ' + transcript
                })
                // Throws error when popup is closed, so this swallows the errors with catch.
                chrome.runtime.sendMessage({
                    message: 'transcriptavailable'
                }).catch(err => ({}))
            })
        }
        else {
            if(send) {
            //No transcript so send to cockroach
                console.log('sending to cockroach')
                chrome.storage.local.get('transcript', data => {
                    console.log(data.transcript)
                })
                send = false
            }
        }
    }
})

chrome.runtime.onMessage.addListener(({ message }) => {
    if(message == 'stop') {
        socket.close()
        alert('Transcription ended')
    }
})