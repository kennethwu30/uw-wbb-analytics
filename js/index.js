document.addEventListener("DOMContentLoaded", () => {
  const url = `./team_metrics.json?v=${Date.now()}`;

  fetch(url)
    .then((r) => {
      if (!r.ok) throw new Error(`Failed to load team_metrics.json: ${r.status}`);
      return r.json();
    })
    .then((data) => {
      // ===== Metric cards =====
      const reboundEl = document.getElementById("rebound-pct");
      const totalEl = document.getElementById("total-attempts");
      const topEl = document.getElementById("top-performer");

      if (reboundEl) reboundEl.textContent = `${Number(data.rebound_percentage).toFixed(1)}%`;
      if (totalEl) totalEl.textContent = `${data.total_good_attempts}/${data.total_attempts}`;
      if (topEl) topEl.textContent = data.top_performer ?? "";

      // ===== Husky Leaders (Top 3) =====
      const leadersTbody = document.getElementById("husky-leaders-tbody");
      const leaders = Array.isArray(data.husky_leaders) ? data.husky_leaders : [];

      if (leadersTbody) {
        leadersTbody.innerHTML = leaders
          .map(
            (p) => `
            <tr>
              <td>${p.Player ?? ""}</td>
              <td class="highlight-purple">${Number(p.success_pct).toFixed(1)}%</td>
            </tr>
          `
          )
          .join("");
      } else {
        console.error("Missing tbody: husky-leaders-tbody");
      }

      // ===== Development Needed (Bottom 3) =====
      const devTbody = document.getElementById("development-needed-tbody");
      const devPlayers = Array.isArray(data.development_needed) ? data.development_needed : [];

      if (devTbody) {
        devTbody.innerHTML = devPlayers
          .map(
            (p) => `
            <tr>
              <td>${p.Player ?? ""}</td>
              <td class="highlight-red">${Number(p.success_pct).toFixed(1)}%</td>
            </tr>
          `
          )
          .join("");
      } else {
        console.error("Missing tbody: development-needed-tbody");
      }

      // ===== Full Roster Breakdown =====
      const rosterTbody = document.getElementById("full-roster-tbody");
      const roster = Array.isArray(data.full_roster) ? data.full_roster : [];

      if (rosterTbody) {
        rosterTbody.innerHTML = roster
          .map((p) => {
            const good = Number(p.good_execution ?? 0);
            const stand = Number(p.stand_around ?? 0);
            const back = Number(p.on_the_back ?? 0);
            const getBack = Number(p.get_back ?? 0);

            // "Total" in your table can just be attempts (recommended)
            const total = Number(p.attempts ?? (good + stand + back + getBack));
            const pct = Number(p.final_pct ?? 0).toFixed(1);

            return `
              <tr>
                <td>${p.Player ?? ""}</td>
                <td>${good}</td>
                <td>${stand}</td>
                <td>${back}</td>
                <td>${getBack}</td>
                <td>${total}</td>
                <td class="highlight-purple">${pct}%</td>
              </tr>
            `;
          })
          .join("");
      } else {
        console.error("Missing tbody: full-roster-tbody");
      }

      console.log("Data loaded:", { url, data });
    })
    .catch((e) => console.error("Error loading team_metrics.json", e));
});