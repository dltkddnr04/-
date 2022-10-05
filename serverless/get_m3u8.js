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
    const api_url = `https://api.twitch.tv/api/channels/${channel}/access_token`
    const api_response = await fetch(api_url, {
        headers: {
            'Client-ID': 'jzkbprff40iqj646a697cyrvl0zt2m6'
        }
    })

    const api_json = await api_response.json()
    const sig = api_json.sig
    const token = api_json.token

    // get ad blocked m3u8

    const m3u8_url = `https://usher.ttvnw.net/api/channel/hls/${channel}.m3u8?sig=${sig}&token=${token}&player=twitchweb&allow_source=true&allow_audio_only=true&allow_spectre=false`
    const m3u8_response = await fetch(m3u8_url)

    return m3u8_response
}