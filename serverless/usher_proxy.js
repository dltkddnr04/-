// simple serverless service to proxy requests to usher
// this service will accept all methods and forward them to usher server

addEventListener('fetch', (event) =>
  event.respondWith(
    handleRequest(event.request).catch(
      (err) => new Response(err.stack, { status: 500 })
    )
  )
)

async function handleRequest(request) {
    const url = new URL(request.url)
    const api_url = `https://usher.ttvnw.net${url.pathname}${url.search}`
    // return api_url
    const api_response = await fetch(api_url)
    return api_response
}