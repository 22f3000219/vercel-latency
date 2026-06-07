from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import numpy as np

app = FastAPI()

TELEMETRY = [{"region":"apac","service":"support","latency_ms":231.64,"uptime_pct":97.626},{"region":"apac","service":"checkout","latency_ms":159.25,"uptime_pct":98.81},{"region":"apac","service":"checkout","latency_ms":178.21,"uptime_pct":97.934},{"region":"apac","service":"recommendations","latency_ms":115.59,"uptime_pct":99.15},{"region":"apac","service":"catalog","latency_ms":155.65,"uptime_pct":97.547},{"region":"apac","service":"analytics","latency_ms":173.88,"uptime_pct":98.706},{"region":"apac","service":"catalog","latency_ms":152.17,"uptime_pct":97.821},{"region":"apac","service":"catalog","latency_ms":148.6,"uptime_pct":98.376},{"region":"apac","service":"catalog","latency_ms":128.35,"uptime_pct":97.431},{"region":"apac","service":"recommendations","latency_ms":183.63,"uptime_pct":98.91},{"region":"apac","service":"catalog","latency_ms":172.26,"uptime_pct":99.48},{"region":"apac","service":"analytics","latency_ms":121.19,"uptime_pct":97.736},{"region":"emea","service":"support","latency_ms":182.23,"uptime_pct":98.032},{"region":"emea","service":"analytics","latency_ms":168.75,"uptime_pct":98.381},{"region":"emea","service":"payments","latency_ms":218.21,"uptime_pct":98.777},{"region":"emea","service":"catalog","latency_ms":202.7,"uptime_pct":97.273},{"region":"emea","service":"catalog","latency_ms":167.57,"uptime_pct":99.368},{"region":"emea","service":"analytics","latency_ms":144.72,"uptime_pct":98.684},{"region":"emea","service":"analytics","latency_ms":133.6,"uptime_pct":99.054},{"region":"emea","service":"analytics","latency_ms":160.59,"uptime_pct":97.941},{"region":"emea","service":"recommendations","latency_ms":115.73,"uptime_pct":99.088},{"region":"emea","service":"payments","latency_ms":180.16,"uptime_pct":98.099},{"region":"emea","service":"checkout","latency_ms":219.39,"uptime_pct":98.793},{"region":"emea","service":"recommendations","latency_ms":126.19,"uptime_pct":99.335},{"region":"amer","service":"analytics","latency_ms":162.28,"uptime_pct":99.31},{"region":"amer","service":"support","latency_ms":209.06,"uptime_pct":98.289},{"region":"amer","service":"recommendations","latency_ms":209.0,"uptime_pct":97.305},{"region":"amer","service":"support","latency_ms":134.65,"uptime_pct":99.451},{"region":"amer","service":"analytics","latency_ms":221.04,"uptime_pct":97.382},{"region":"amer","service":"payments","latency_ms":212.9,"uptime_pct":98.686},{"region":"amer","service":"support","latency_ms":215.93,"uptime_pct":99.299},{"region":"amer","service":"catalog","latency_ms":214.43,"uptime_pct":98.106},{"region":"amer","service":"payments","latency_ms":196.75,"uptime_pct":97.275},{"region":"amer","service":"analytics","latency_ms":103.77,"uptime_pct":98.1},{"region":"amer","service":"checkout","latency_ms":190.82,"uptime_pct":98.426},{"region":"amer","service":"analytics","latency_ms":105.87,"uptime_pct":99.235}]

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

@app.options("/")
async def options():
    return JSONResponse(content={}, headers=CORS_HEADERS)

@app.post("/")
async def analyze(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)
    result = {}
    for region in regions:
        records = [r for r in TELEMETRY if r["region"] == region]
        if not records:
            result[region] = {}
            continue
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 4),
            "p95_latency": round(float(np.percentile(latencies, 95)), 4),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > threshold_ms))
        }
    return JSONResponse(content=result, headers=CORS_HEADERS)
