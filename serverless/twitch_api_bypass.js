// simple access token server run on cloudflare workers

addEventListener('fetch', (event) =>
    event.respondWith(
        handleRequest(event.request).catch(
            (err) => new Response(err.stack, { status: 500 })
        )
    )
)

async function getAccessToken() {
    const client_id = '5ayor8kn22hxinl6way2j1ejzi41g2'
    const client_secret = '8tp18ssnpzbrzyyf0he83q3lsfayyx'
    const api_url = `https://id.twitch.tv/oauth2/token?client_id=${client_id}&client_secret=${client_secret}&grant_type=client_credentials`
    const api_response = await fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    const api_json = await api_response.json()
    const access_token = api_json.access_token

    const access_header = {
        'Client-ID': client_id,
        'Authorization': `Bearer ${access_token}`
    }

    return access_header
}

async function handleRequest(request) {
    // get url params
    const url = new URL(request.url)
    const path = url.pathname
    const params = url.searchParams
}