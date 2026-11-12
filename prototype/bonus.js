(() => {
  const el = id => document.getElementById(id);
  const run = el('live-run');
  const status = el('live-status');
  const download = el('live-download');
  let config, record, activeSignature, busy = false;
  const context = () => ({ caseId: el('case').value, missing: el('missing').checked, pressure: el('case').value === 'S02' && el('pressure').checked });
  const signature = () => JSON.stringify(context());
  const labels = { discrepancy: 'Có chênh lệch cần người xem xét', insufficient_evidence: 'Chưa đủ căn cứ xác định sai mô tả', source_missing: 'Thiếu mô tả lúc đặt' };
  const steps = { human_review: 'Chuyển người xem xét', ask_evidence: 'Bổ sung chứng cứ cụ thể', explain_limits: 'Giải thích căn cứ và giới hạn' };
  window.refreshLiveAnalysis = () => {
    if (activeSignature && signature() !== activeSignature) {
      record = null;
      download.hidden = true;
      el('live-evidence').replaceChildren();
      status.textContent = 'Dữ liệu đã đổi. Cần gọi AI lại; kết quả trước không áp dụng cho hồ sơ này.';
    }
  };
  run.addEventListener('click', async () => {
    if (busy) return;
    if (location.protocol === 'file:') {
      status.textContent = 'Chạy python -m prototype.server và mở http://127.0.0.1:3000 để dùng AI thật.';
      return;
    }
    busy = true; run.disabled = true; record = null; download.hidden = true;
    el('live-evidence').replaceChildren();
    activeSignature = signature();
    status.textContent = 'Đang gọi OpenRouter bằng model miễn phí…';
    try {
      config = await fetch('/api/config').then(r => { if (!r.ok) throw new Error('Không kết nối được máy chủ demo.'); return r.json(); });
      if (!config.configured) throw new Error('Chưa có OPENROUTER_API_KEY trên máy chủ. Chưa gọi AI thật.');
      const response = await fetch('/api/analyze', {
        method: 'POST', signal: AbortSignal.timeout(90000),
        headers: { 'Content-Type': 'application/json', 'X-Demo-Token': config.token },
        body: activeSignature
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error + (data.code ? ` (${data.code})` : ''));
      if (signature() !== activeSignature) { status.textContent = 'Dữ liệu đã đổi trong lúc AI xử lý. Hãy gọi lại với hồ sơ mới.'; return; }
      record = data;
      status.textContent = `AI thật · ${data.model} · ${data.response_id} · ${data.duration_ms} ms. ${labels[data.result.assessment]}. Bước đề xuất: ${steps[data.result.next_step]}.`;
      const summary = document.createElement('li');
      summary.textContent = data.result.summary;
      const quotes = data.result.evidence.map(item => {
        const row = document.createElement('li'); row.textContent = `${item.source_id}: “${item.quote}”`; return row;
      });
      el('live-evidence').replaceChildren(summary, ...quotes);
      download.hidden = false;
    } catch (error) {
      const message = error.name === 'TimeoutError' ? 'Hết thời gian chờ kết quả từ máy chủ.' : error.message;
      status.textContent = `AI thật chưa hoàn tất: ${message} Luồng mô phỏng vẫn dùng được; chưa hoàn/đóng/phạt.`;
    } finally { busy = false; run.disabled = false; }
  });
  download.addEventListener('click', () => {
    if (!record || signature() !== activeSignature) return;
    const url = URL.createObjectURL(new Blob([JSON.stringify(record, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a'); a.href = url; a.download = `ai-evidence-${record.run_id}.json`; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})();
