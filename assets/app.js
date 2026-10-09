"use strict";
const els = {
  results: document.getElementById("results"),
  count: document.getElementById("count"),
  query: document.getElementById("query"),
  platform: document.getElementById("platform"),
  genre: document.getElementById("genre"),
  content: document.getElementById("content"),
};
const label = {
  arcade: "오락실·레트로", playstation: "PlayStation", pc: "PC",
  mobile: "모바일", "other-console": "기타 콘솔",
  rts: "RTS", moba: "MOBA", "battle-royale": "배틀로얄",
  platformer: "플랫포머",
  "official-info": "공식 게임 정보",
  "developer-diary": "제작 이야기",
  "official-trailer": "공식 트레일러",
  "official-ending": "공식 엔딩",
  esports: "e스포츠",
};
const urlParameters = new URLSearchParams(window.location.search);
let games = [];
let opened = new Set();
let revealed = new Set();
const node = (tag, className, text) => {
  const x = document.createElement(tag);
  if (className) x.className = className;
  if (text !== undefined) x.textContent = text;
  return x;
};
function verifiedLink(url) {
  try {
    const u = new URL(url);
    return u.protocol === "https:" &&
      ["www.playstation.com", "www.pubg.com", "pacman.com", "www.pacman.com"].includes(u.hostname) ? u.href : null;
  } catch { return null; }
}
function detailPanel(game) {
  const panel = node("div", "detail");
  const heading = node("h4", "", "확인된 공식 자료");
  panel.append(heading);
  if (!game.materials?.length) {
    panel.append(node("p", "detail-note", "아직 검증된 개별 자료가 없습니다. 공식 영상·엔딩·공략은 출처 검증 후 등록됩니다."));
  }
  for (const material of game.materials || []) {
    const isSpoiler = material.spoiler === true;
    const wrap = node("div", isSpoiler && !revealed.has(game.id + ":" + material.title) ? "spoiler" : "resource");
    if (isSpoiler && !revealed.has(game.id + ":" + material.title)) {
      wrap.append(node("div", "", "⚠ 스토리·엔딩 스포일러가 포함된 자료입니다."));
      const reveal = node("button", "", "내용 표시");
      reveal.type = "button";
      reveal.addEventListener("click", () => {
        revealed.add(game.id + ":" + material.title);
        render();
      });
      wrap.append(reveal);
    } else {
      const info = node("div", "resource-info");
      info.append(node("strong", "", material.title));
      info.append(node("span", "", (label[material.type] || material.type) + " · " + material.publisher));
      wrap.append(info);
      const link = verifiedLink(material.url);
      if (link) {
        const a = node("a", "", "공식 페이지 ↗");
        a.href = link; a.target = "_blank"; a.rel = "noopener noreferrer";
        wrap.append(a);
      }
    }
    panel.append(wrap);
  }
  if (!game.materials?.some(m => m.type === "official-ending")) {
    panel.append(node("p", "detail-note", "엔딩 영상: 검증·등록 대기 중 (등록되지 않은 콘텐츠는 검색 결과에도 표시하지 않습니다)."));
  }
  return panel;
}
function render() {
  const q = els.query.value.trim().toLocaleLowerCase();
  const matches = games.filter(g => {
    const text = [g.name, g.english, ...(g.aliases || [])].join(" ").toLocaleLowerCase();
    const allMaterials = g.materials || [];
    return (!q || text.includes(q)) &&
      (els.platform.value === "all" || g.platforms.includes(els.platform.value)) &&
      (els.genre.value === "all" || g.genres.includes(els.genre.value)) &&
      (els.content.value === "all" || allMaterials.some(m => m.type === els.content.value));
  });
  els.results.replaceChildren();
  els.count.textContent = matches.length + "개 작품";
  if (!matches.length) {
    els.results.append(node("div", "empty", "선택한 조건에 해당하는 검증된 자료가 없습니다. 다른 검색어·필터를 선택해 보세요."));
    return;
  }
  for (const game of matches) {
    const card = node("article", "game-card");
    const top = node("div", "card-top");
    top.append(node("span", "mini-art", game.symbol || "🎮"));
    top.append(node("span", "tag", "시범 목록"));
    card.append(top, node("h3", "", game.name), node("div", "subtitle", game.english));
    card.append(node("p", "", game.description));
    const chips = node("div", "chips");
    [...game.platforms, ...game.genres].slice(0, 4).forEach(p => chips.append(node("span", "chip", label[p] || p)));
    card.append(chips);
    if (typeof game.detail_path === "string" && /^games\/[a-z0-9]+(?:-[a-z0-9]+)*\/$/.test(game.detail_path)) {
      const link = node("a", "detail-link", "고정 주소로 상세 보기 ↗");
      link.href = "./" + game.detail_path;
      card.append(link);
    }
    const button = node("button", "expand", opened.has(game.id) ? "상세 정보 접기 ↑" : "작품 상세·공식 자료 보기 ↓");
    button.type = "button";
    button.setAttribute("aria-expanded", String(opened.has(game.id)));
    button.addEventListener("click", () => {
      if (opened.has(game.id)) opened.delete(game.id); else opened.add(game.id);
      render();
      const fresh = els.results.querySelector('[data-game-id="' + game.id + '"] .expand');
      if (fresh) fresh.focus();
    });
    card.dataset.gameId = game.id;
    card.append(button);
    if (opened.has(game.id)) card.append(detailPanel(game));
    els.results.append(card);
  }
}
async function init() {
  try {
    const res = await fetch("./data/sample-games.json", {cache:"no-store"});
    if (!res.ok) throw new Error("status " + res.status);
    const payload = await res.json();
    if (!Array.isArray(payload.games)) throw new Error("invalid game catalog");
    games = payload.games;
    // Preserve historical root/query URLs. Do not silently redirect iframe or shared links.
    // These optional query parameters enhance discovery; the path itself stays valid.
    const oldGameKey = urlParameters.get("game") || urlParameters.get("slug") || urlParameters.get("id");
    if (oldGameKey) {
      const match = games.find(g => [g.id, g.name, g.english, ...(g.aliases || [])]
        .some(key => String(key).toLocaleLowerCase() === oldGameKey.toLocaleLowerCase()));
      if (match) {
        els.query.value = match.name;
        opened.add(match.id);
      }
    } else if (urlParameters.get("q")) {
      els.query.value = urlParameters.get("q").slice(0, 200);
    }
    [els.query, els.platform, els.genre, els.content].forEach(el => el.addEventListener("input", render));
    render();
  } catch (err) {
    els.count.textContent = "데이터 불러오기 실패";
    els.results.replaceChildren(node("p", "empty", "시범 목록을 불러올 수 없습니다. 웹서버에서 페이지를 열어 다시 확인해 주세요."));
    console.error("public sample catalog load failed:", err.message);
  }
}
init();
