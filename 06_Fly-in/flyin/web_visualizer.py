# flake8: noqa
"""Standalone HTML visualisation of a completed schedule."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import cast

from .schedule import Schedule


class WebVisualizer:
    """Write an interactive SVG replay for a schedule."""

    def render(self, schedule: Schedule, output_path: str) -> None:
        flight_map = schedule.flight_map
        zones = list(flight_map.zones.values())
        if zones:
            min_x = min(zone.x for zone in zones)
            max_x = max(zone.x for zone in zones)
            min_y = min(zone.y for zone in zones)
            max_y = max(zone.y for zone in zones)
            span_x = max(max_x - min_x, 1)
            span_y = max(max_y - min_y, 1)
        else:
            min_x = min_y = span_x = span_y = 0

        def point(zone_name: str) -> list[int]:
            zone = flight_map.zone(zone_name)
            x = 90 + (zone.x - min_x) / span_x * 820
            y = 90 + (zone.y - min_y) / span_y * 470
            return [round(x), round(y)]

        nodes = []
        for name, zone in flight_map.zones.items():
            nodes.append({
                "id": name,
                "x": point(name)[0],
                "y": point(name)[1],
                "type": zone.zone_type.value,
                "color": zone.color or "#8fa7bf",
                "start": zone.is_start,
                "end": zone.is_end,
            })

        connections = []
        for connection in flight_map.connections:
            connections.append({
                "id": connection.name,
                "a": connection.zone_a,
                "b": connection.zone_b,
                "capacity": connection.max_link_capacity,
            })

        positions = {drone: flight_map.start for drone in range(1, flight_map.nb_drones + 1)}
        flights: dict[int, dict[str, object]] = {}
        trails: dict[int, list[list[str]]] = {drone: [] for drone in positions}
        turns = []
        grouped = schedule.moves_by_turn()

        for turn in range(1, schedule.total_turns + 1):
            for drone, move in grouped.get(turn, []):
                previous = positions.get(drone)
                if move.is_transit:
                    current = positions.pop(drone, None)
                    if current:
                        flights[drone] = {
                            "connection": move.destination,
                            "from": current,
                            "to": move.target_zone or "?",
                            "departure": turn,
                            "arrival": move.arrival_turn,
                        }
                    continue
                in_flight = flights.pop(drone, None)
                origin = previous
                if in_flight is not None:
                    origin = str(in_flight["from"])
                if origin is not None and origin != move.destination:
                    trails[drone].append([origin, move.destination])
                positions[drone] = move.destination

            frame_flights = []
            for drone, flight in flights.items():
                departure = cast(int, flight["departure"])
                arrival = cast(int, flight["arrival"])
                duration = max(arrival - departure, 1)
                progress = min(max((turn - departure) / duration, 0), 1)
                frame_flights.append({
                    "drone": drone,
                    "from": flight["from"],
                    "to": flight["to"],
                    "progress": progress,
                })

            frame_positions = []
            for drone, zone_name in positions.items():
                frame_positions.append({"drone": drone, "zone": zone_name})
            turns.append({
                "turn": turn,
                "zones": frame_positions,
                "flights": frame_flights,
                "trails": trails.copy(),
            })

        data = {
            "title": html.escape(f"Fly-in - {flight_map.nb_drones} drones"),
            "nodes": nodes,
            "connections": connections,
            "turns": turns,
        }
        payload = json.dumps(data, ensure_ascii=True).replace("</", "<\\/")
        Path(output_path).write_text(self._template(payload), encoding="utf-8")

    def _template(self, payload: str) -> str:
        return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fly-in route replay</title>
<style>
:root { color-scheme: dark; --ink:#dce7f3; --panel:#11151b; --muted:#8796a8; }
* { box-sizing:border-box; }
body { margin:0; min-height:100vh; overflow:hidden; background:#080b0f; color:var(--ink); font-family:"Trebuchet MS",sans-serif; }
header { height:76px; display:flex; align-items:center; justify-content:space-between; padding:0 28px; border-bottom:1px solid #28303a; }
h1 { margin:0; font-size:22px; letter-spacing:0; }
.controls { display:flex; align-items:center; gap:10px; }
button { width:38px; height:38px; border:1px solid #3a4654; border-radius:6px; background:#171d25; color:white; cursor:pointer; font-size:16px; }
button:hover { background:#263141; }
#turn { min-width:108px; text-align:center; font:700 16px/38px monospace; }
main { height:calc(100vh - 76px); display:grid; grid-template-columns:minmax(0,1fr) 220px; }
svg { width:100%; height:100%; }
aside { padding:18px 16px; border-left:1px solid #28303a; background:var(--panel); overflow:auto; }
.legend { display:grid; gap:14px; font-size:13px; }
.item { display:flex; align-items:center; gap:10px; }
.dot { width:14px; height:14px; border-radius:50%; border:1px solid #dbe8f5; }
.link { width:28px; height:3px; }
.stats { margin-top:24px; padding-top:16px; border-top:1px solid #303844; color:var(--muted); line-height:1.8; }
.node text { fill:#10243b; font-size:17px; font-weight:700; text-anchor:middle; dominant-baseline:middle; pointer-events:none; }
.node-label { fill:#8e9bad; font-size:12px; text-anchor:middle; }
.edge { stroke:#5b6470; stroke-width:5; opacity:.8; }
.trail { fill:none; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; }
.drone { stroke:#080b0f; stroke-width:3; filter:drop-shadow(0 2px 5px #000); }
.cap-label { fill:#99a8ba; font-size:11px; text-anchor:middle; }
@media (max-width:760px) { body { overflow:auto; } header { padding:0 12px; } h1 { font-size:18px; } main { height:auto; min-height:calc(100vh - 76px); grid-template-columns:1fr; } svg { height:58vh; min-height:390px; } aside { border-left:0; border-top:1px solid #28303a; } }
</style>
</head>
<body>
<header><h1 id="title">Fly-in route replay</h1><div class="controls"><button id="prev" aria-label="Previous turn">&#9664;</button><button id="play" aria-label="Play replay">&#9654;</button><button id="next" aria-label="Next turn">&#9654;&#9654;</button><span id="turn">Turn: 0</span></div></header>
<main><svg id="map" viewBox="0 0 1000 650" role="img" aria-label="Animated drone route map"></svg><aside><div class="legend"><div class="item"><span class="dot" style="background:#f7fbff"></span>Start / end</div><div class="item"><span class="dot" style="background:#c6d6e8"></span>Normal zone</div><div class="item"><span class="dot" style="background:#f4a261"></span>Priority zone</div><div class="item"><span class="dot" style="background:#fff0d1;border-style:dashed"></span>Restricted zone</div><div class="item"><span class="dot" style="background:#2c343e;border-color:#718096"></span>Blocked zone</div><div class="item"><span class="link" style="background:#8b5cf6"></span>Drones</div></div><div class="stats" id="stats"></div></aside></main>
<script>
const data = __DATA__;
document.getElementById('title').textContent = data.title;
const svg = document.getElementById('map');
const NS = 'http://www.w3.org/2000/svg';
const nodeMap = Object.fromEntries(data.nodes.map(n => [n.id, n]));
const palette = ['#8b5cf6','#ff7f50','#21c7a8','#f6c453','#ef5da8','#55a8ff'];
let index = 0;
let timer = null;
function el(name, attrs={}) { const e=document.createElementNS(NS,name); Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v)); return e; }
function drawBase() {
 svg.replaceChildren();
 data.connections.forEach(c=>{ const a=nodeMap[c.a], b=nodeMap[c.b]; svg.append(el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'edge'})); const mx=(a.x+b.x)/2, my=(a.y+b.y)/2; const label=el('text',{x:mx,y:my-8,class:'cap-label'}); label.textContent=c.capacity>1 ? c.capacity+' places' : ''; svg.append(label); });
 data.nodes.forEach(n=>{ const g=el('g',{class:'node'}); let fill=n.start||n.end?'#f7fbff':n.type==='restricted'?'#fff0d1':n.type==='priority'?'#f4a261':n.type==='blocked'?'#30343b':n.color||'#c6d6e8'; const circle=el('circle',{cx:n.x,cy:n.y,r:36,fill,stroke:n.start?'#6ee7ff':n.end?'#22c55e':'#eef4ff','stroke-width':n.start||n.end?5:3}); if(n.type==='restricted') circle.setAttribute('stroke-dasharray','5 5'); g.append(circle); const text=el('text',{x:n.x,y:n.y}); text.textContent=n.id; g.append(text); const label=el('text',{x:n.x,y:n.y+52,class:'node-label'}); label.textContent=n.start?'START':n.end?'END':n.type.toUpperCase(); g.append(label); svg.append(g); });
 svg.append(el('g',{id:'trails'})); svg.append(el('g',{id:'drones'}));
}
function render() {
 document.getElementById('trails').replaceChildren(); document.getElementById('drones').replaceChildren();
 const frame=data.turns[index]; document.getElementById('turn').textContent='Turno: '+frame.turn;
 const occupied=new Map(); frame.zones.forEach(p=>{occupied.set(p.zone,(occupied.get(p.zone)||0)+1)});
 Object.entries(frame.trails||{}).forEach(([drone,trails])=>{ trails.forEach((edge,trailIndex)=>{ const a=nodeMap[edge[0]],b=nodeMap[edge[1]]; if(!a||!b)return; const opacity=.18+(trailIndex/Math.max(trails.length,1))*0.58; const line=el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'trail',stroke:palette[(Number(drone)-1)%palette.length],'stroke-opacity':opacity}); document.getElementById('trails').append(line); }); });
 frame.zones.forEach(p=>{const n=nodeMap[p.zone]; drawDrone(p.drone,n.x,n.y)});
 frame.flights.forEach(f=>{const a=nodeMap[f.from],b=nodeMap[f.to]; if(!a||!b)return; const x=a.x+(b.x-a.x)*f.progress,y=a.y+(b.y-a.y)*f.progress; drawDrone(f.drone,x,y);});
 document.getElementById('stats').innerHTML=`<strong>Turno ${frame.turn}/${data.turns.length}</strong><br>${data.nodes.length} zonas<br>${data.connections.length} conexoes<br>${data.turns[0].zones.length + frame.flights.length} drones ativos`;
}
function drawDrone(id,x,y) { const g=el('g',{class:'drone-group'}), circle=el('circle',{cx:x,cy:y,r:14,fill:palette[(id-1)%palette.length],class:'drone'}); g.append(circle); const text=el('text',{x:x,y:y+4,fill:'#10141a','font-size':'10','font-weight':'700','text-anchor':'middle'}); text.textContent=id; g.append(text); document.getElementById('drones').append(g); }
function stop(){if(timer){clearInterval(timer);timer=null;document.getElementById('play').innerHTML='&#9654;';}}
document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};
document.getElementById('next').onclick=()=>{stop();index=Math.min(data.turns.length-1,index+1);render()};
document.getElementById('play').onclick=()=>{if(timer){stop();return;}if(index>=data.turns.length-1)index=0; document.getElementById('play').innerHTML='&#10074;&#10074;';timer=setInterval(()=>{if(index<data.turns.length-1){index++;render()}else stop()},850)};
document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key===' ')document.getElementById('play').click();});
drawBase(); render();
</script>
</body>
</html>
""".replace("__DATA__", payload)
