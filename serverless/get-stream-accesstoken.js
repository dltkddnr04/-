// simple proxy server run on cloudflare workers

addEventListener('fetch', (event) =>
  event.respondWith(
    handleRequest(event.request).catch(
      (err) => new Response(err.stack, { status: 500 })
    )
  )
)

async function handleRequest(request) {
    const url = new URL(request.url)
    const channel = url.searchParams.get('channel')
    const api_url = `https://gql.twitch.tv/gql#origin=twilight`
    const data = {
        operationName: "PlaybackAccessToken",
        variables: {
            isLive: true,
            login: channel,
            isVod: false,
            vodID: "",
            playerType: "frontpage"
        },
        extensions: {
            persistedQuery: {
                version: 1,
                sha256Hash: "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
            }
        }
    }

    // get access token using api include data
    const get_access_token = await fetch(api_url, {
        method: 'POST',
        headers: {
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko'
        },
        body: JSON.stringify(data)
    })

    const api_json = await get_access_token.json()
    const token = api_json.data.streamPlaybackAccessToken.value
    const sig = api_json.data.streamPlaybackAccessToken.signature

    return new Response(JSON.stringify({token, sig}), {
        headers: {
            'Content-Type': 'application/json'
        }
    })
}