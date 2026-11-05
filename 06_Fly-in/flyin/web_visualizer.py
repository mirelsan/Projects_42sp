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
                "capacity": flight_map.capacity(name),
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

        routes = {}
        for trajectory in schedule.trajectories:
            route = [flight_map.start]
            for move in trajectory.moves:
                destination = (
                    move.target_zone
                    if move.is_transit and move.target_zone
                    else move.destination
                )
                if destination != route[-1]:
                    route.append(destination)
            routes[trajectory.drone_id] = route

        data = {
            "title": html.escape(f"Fly-in - {flight_map.nb_drones} drones"),
            "mapName": html.escape(output_path.rsplit("/", 1)[-1]),
            "droneCount": flight_map.nb_drones,
            "totalTurns": schedule.total_turns,
            "nodes": nodes,
            "connections": connections,
            "turns": turns,
            "routes": routes,
        }
        payload = json.dumps(data, ensure_ascii=True).replace("</", "<\\/")
        Path(output_path).write_text(self.template(payload), encoding="utf-8")

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

    def template(self, payload: str) -> str:
        """Return the single-file dark replay interface."""
        return """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fly-in replay</title>
<style>
:root{color-scheme:dark;--bg:#090b12;--panel:#111521;--line:#293047;--ink:#f6f8ff;--muted:#9ca8c0;--purple:#a855f7}
*{box-sizing:border-box}body{margin:0;height:100vh;overflow:hidden;background:var(--bg);color:var(--ink);font-family:Inter,"Segoe UI",sans-serif}
header{height:76px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:22px}.map-name{color:var(--muted);font-size:14px}
.controls{display:flex;align-items:center;gap:9px}button{width:40px;height:40px;border:1px solid var(--line);border-radius:6px;background:#171c28;color:white;cursor:pointer;font-size:16px}button:hover{background:#242b3d}
#turn-label{min-width:96px;text-align:center;font-weight:700;font-size:14px}
main{height:calc(100vh - 76px);display:grid;grid-template-columns:minmax(0,1fr) 300px}section{position:relative;overflow:hidden}
#map{width:100%;height:100%;background:radial-gradient(circle at 50% 45%,#111827 0,#090b12 70%)}
aside{padding:18px 22px;border-left:1px solid var(--line);background:var(--panel);overflow:auto}h2{margin:0 0 18px;color:var(--muted);font-size:12px;font-weight:500;text-transform:uppercase;letter-spacing:.12em}
.legend{display:grid;gap:13px;font-size:14px;margin-bottom:28px}.item{display:flex;align-items:center;gap:12px;color:#d9deeb}
.dot{width:16px;height:16px;border-radius:50%;border:2px solid var(--ink)}.dot.start{border-color:#67d5ff;box-shadow:0 0 14px #67d5ff66}.dot.end{border-color:#25d7a0;box-shadow:0 0 14px #25d7a066}.dot.priority{background:#ffad32}.dot.restricted{border-style:dashed}.dot.blocked{background:#2d3448;border-color:#8993aa}
.trail-key{width:30px;height:4px;background:var(--purple)}.trail-key.future{background:repeating-linear-gradient(90deg,var(--purple) 0 7px,transparent 7px 12px)}
.selected{min-height:150px;padding-top:16px;border-top:1px solid var(--line)}#selection{line-height:1.9}.stats{margin-top:22px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);line-height:1.9;font-size:14px}
.edge{stroke:#58657d;stroke-width:2;opacity:.65}.edge.used{stroke:#b469ff;stroke-width:6;opacity:1}.trail{fill:none;stroke:var(--purple);stroke-width:7;stroke-linecap:round;opacity:.82}.trail.future{stroke-width:5;stroke-dasharray:2 13}
.node{cursor:pointer}.node circle{stroke:#e6edf8;stroke-width:2}.node.start circle{stroke:#67d5ff;stroke-width:7}.node.end circle{stroke:#25d7a0;stroke-width:7}.node.priority circle{stroke:#ffad32;stroke-width:5}.node.restricted circle{stroke-dasharray:5 5}.node.blocked circle{fill:#202535;stroke:#74809b}
.node-label{fill:#fff;stroke:#090b12;stroke-width:4px;paint-order:stroke;stroke-linejoin:round;font-size:13px;font-weight:700;text-anchor:middle}.badge{fill:#111521;stroke:#a855f7;stroke-width:1}.badge-text{fill:#fff;font-size:10px;font-weight:700;text-anchor:middle}
.drone circle{stroke:#090b12;stroke-width:2}.drone text{fill:white;font-size:9px;font-weight:800;text-anchor:middle;dominant-baseline:middle}
.progress{position:absolute;left:0;right:0;bottom:0;height:5px;background:#1d2230}.progress span{display:block;height:100%;background:linear-gradient(90deg,#7c3aed,#c084fc)}#progress-input{position:absolute;inset:-8px 0;width:100%;opacity:0;cursor:pointer}
@media(max-width:800px){main{grid-template-columns:1fr}aside{display:none}}
</style>
</head>
<body>
<header><div><h1 id="title">Fly-in replay</h1><span class="map-name" id="map-name"></span></div><div class="controls"><button id="prev">&#9664;</button><button id="play">&#9654;</button><button id="next">&#9654;&#9654;</button><span id="turn-label">Turno 0/0</span></div></header>
<main><section><svg id="map" viewBox="0 0 1000 650"></svg><div class="progress"><span id="progress-fill"></span><input id="progress-input" type="range" min="0" max="0" value="0"></div></section><aside><h2>Lenda</h2><div class="legend"><div class="item"><span class="dot start"></span>Inicio</div><div class="item"><span class="dot end"></span>Fim</div><div class="item"><span class="dot"></span>Normal</div><div class="item"><span class="dot priority"></span>Prioridade</div><div class="item"><span class="dot restricted"></span>Restrita</div><div class="item"><span class="dot blocked"></span>Bloqueada</div><div class="item"><span class="trail-key"></span>Rota percorrida</div><div class="item"><span class="trail-key future"></span>Rota futura</div></div><div class="selected"><h2>Zona selecionada</h2><div id="selection">Clique em uma zona.</div></div><div class="stats" id="stats"></div></aside></main>
<script>
const data=__DATA__,NS='http://www.w3.org/2000/svg',svg=document.getElementById('map');
const nodes=Object.fromEntries(data.nodes.map(n=>[n.id,n])),palette=['#a855f7','#ef5da8','#55a8ff','#21c7a8','#f6c453','#fb7185'];
let index=0,timer=null;
function el(name,attrs={}){const e=document.createElementNS(NS,name);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));return e}
function safeColor(value){const c=document.createElement('canvas').getContext('2d');c.fillStyle='#';c.fillStyle=value||'';return c.fillStyle==='#000000'||c.fillStyle===''?'#8996ad':value}
function drawBase(){
 svg.replaceChildren();
 data.connections.forEach(c=>{const a=nodes[c.a],b=nodes[c.b];svg.append(el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'edge',id:'edge-'+c.id.replace(/[^a-z0-9]/gi,'-')}))});
 data.nodes.forEach(n=>{const g=el('g',{class:'node '+(n.start?'start ':n.end?'end ':'')+n.type});g.dataset.name=n.id;
 const circle=el('circle',{cx:n.x,cy:n.y,r:n.start||n.end?28:21,fill:safeColor(n.color)});g.append(circle);
 const tooltip=el('title');tooltip.textContent=n.id;g.append(tooltip);
 if(n.start||n.end){const t=el('text',{x:n.x,y:n.y+38,class:'node-label'});t.textContent=n.id;g.append(t)}
 g.onclick=()=>selectZone(n.id);svg.append(g)});
 svg.append(el('g',{id:'trails'}));svg.append(el('g',{id:'drones'}));
}
let selectedZone=null;
function selectZone(name){
 selectedZone=name;const n=nodes[name],used=occupiedCount(name);
 document.getElementById('selection').innerHTML='<strong>'+shortName(name)+'</strong><br>Tipo: '+n.type+'<br>Cor: '+(n.color||'padrao')+'<br>Capacidade: '+used+'/'+n.capacity+' drones';
 renderFixedLabels();
}
function shortName(name){return name.length<=18?name:name.slice(0,17)+'...'}
function renderFixedLabels(){
 svg.querySelectorAll('.selected-label').forEach(label=>label.remove());
 if(!selectedZone)return;
 const n=nodes[selectedZone];
 if(!n.start&&!n.end){
  const label=el('text',{x:n.x,y:n.y+38,class:'node-label selected-label'});
  label.textContent=shortName(n.id);
  svg.append(label);
 }
 const placed=[];
 svg.querySelectorAll('.node-label').forEach(label=>{
  let x=Number(label.getAttribute('x')), y=Number(label.getAttribute('y'));
  let attempt=0;
  while(placed.some(p=>Math.abs(p.x-x)<95&&Math.abs(p.y-y)<16)&&attempt<5){y+=18;attempt++}
  label.setAttribute('y',y);
  placed.push({x,y});
 });
}
function occupiedCount(name){const frame=data.turns[index];return frame.zones.filter(p=>p.zone===name).length}
function render(){
 document.getElementById('trails').replaceChildren();document.getElementById('drones').replaceChildren();
 const frame=data.turns[index],progress=data.turns.length?index/(data.turns.length-1)*100:0;
 document.getElementById('turn-label').textContent='Turno '+frame.turn+'/'+data.totalTurns;
 document.getElementById('progress-fill').style.width=progress+'%';document.getElementById('progress-input').max=data.turns.length-1;document.getElementById('progress-input').value=index;
 document.querySelectorAll('.edge.used').forEach(e=>e.classList.remove('used'));
 Object.entries(frame.trails||{}).forEach(([id,trails])=>trails.forEach(edge=>{const a=nodes[edge[0]],b=nodes[edge[1]];if(a&&b)document.getElementById('trails').append(el('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'trail'}))}));
 frame.zones.forEach(p=>{const n=nodes[p.zone];drawDrone(p.drone,n.x,n.y)});
 frame.flights.forEach(f=>{const a=nodes[f.from],b=nodes[f.to];drawDrone(f.drone,a.x+(b.x-a.x)*f.progress,a.y+(b.y-a.y)*f.progress)});
 const current={};frame.zones.forEach(p=>current[p.zone]=(current[p.zone]||0)+1);
 Object.entries(current).forEach(([name,count])=>{const n=nodes[name],dx=n.x+19,dy=n.y-19;const badge=document.createElementNS(NS,'g');const label=count+'/'+n.capacity;badge.append(el('rect',{x:dx-10,y:dy-7,width:20+label.length*4,height:14,rx:7,class:'badge'}));const text=el('text',{x:dx+label.length*2,y:dy+3,class:'badge-text'});text.textContent=label;badge.append(text);svg.append(badge)});
 document.getElementById('stats').innerHTML='<strong>Turno '+frame.turn+'/'+data.totalTurns+'</strong><br>'+data.nodes.length+' zonas · '+data.connections.length+' conexoes<br>'+data.droneCount+' drones';
 renderFixedLabels();
}
function drawDrone(id,x,y){const g=el('g',{class:'drone'}),circle=el('circle',{cx:x,cy:y,r:12,fill:palette[(id-1)%palette.length]});g.append(circle);const text=el('text',{x,y:y+0});text.textContent=id;g.append(text);document.getElementById('drones').append(g)}
function stop(){if(timer){clearInterval(timer);timer=null;document.getElementById('play').innerHTML='&#9654;'}}
document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(data.turns.length-1,index+1);render()};
document.getElementById('play').onclick=()=>{if(timer){stop();return}if(index>=data.turns.length-1)index=0;document.getElementById('play').innerHTML='&#10074;&#10074;';timer=setInterval(()=>{if(index<data.turns.length-1){index++;render()}else stop()},850)};
document.getElementById('progress-input').oninput=e=>{stop();index=Number(e.target.value);render()};
document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key===' ') {e.preventDefault();document.getElementById('play').click()}});
document.getElementById('title').textContent=data.title;drawBase();render();
</script>
</body>
</html>""".replace("__DATA__", payload)
