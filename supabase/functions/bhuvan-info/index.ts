// Supabase Edge Function: CORS proxy for Bhuvan WMS GetFeatureInfo only.
const ALLOWED_PREFIX = "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms?";
const cors = {
  "Access-Control-Allow-Origin": "https://pievenus.github.io",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const target = new URL(req.url).searchParams.get("u") || "";
  if (!target.startsWith(ALLOWED_PREFIX) || !/request=getfeatureinfo/i.test(target)) {
    return new Response("Only Bhuvan GetFeatureInfo requests are allowed", { status: 400, headers: cors });
  }
  try {
    const r = await fetch(target, { signal: AbortSignal.timeout(15000) });
    const text = (await r.text()).slice(0, 20000);
    return new Response(text, { status: r.status, headers: { ...cors, "Content-Type": "text/plain; charset=utf-8" } });
  } catch (_e) {
    return new Response("Bhuvan did not respond", { status: 502, headers: cors });
  }
});
