"""Local-only FastAPI server. Run: python -m prototype.server."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import secrets
from time import perf_counter
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import httpx
import uvicorn

from .ai import analyze, make_input

ROOT = Path(__file__).resolve().parent
ERROR_MESSAGES = {
    "OUTPUT_TOKEN_LIMIT": "Model đã dùng hết ngân sách token trước khi trả JSON hoàn chỉnh. Hãy thử lại hoặc chọn một model :free khác trong .env rồi khởi động lại máy chủ.",
    "INCOMPLETE_RESPONSE": "OpenRouter chưa trả phản hồi hoàn chỉnh. Chưa ghi nhận kết quả AI thật.",
    "INVALID_PROVIDER_RESPONSE": "OpenRouter trả dữ liệu không đọc được; hãy thử lại sau.",
    "EMPTY_MODEL_OUTPUT": "Model không trả nội dung phân tích. Hãy thử lại hoặc chọn model :free khác.",
    "INVALID_MODEL_JSON": "Model trả JSON không hợp lệ; kết quả đã bị chặn, không dùng làm căn cứ.",
    "INVALID_OUTPUT": "Kết quả AI không đúng cấu trúc yêu cầu; kết quả đã bị chặn.",
    "INVALID_EVIDENCE": "AI trích nguồn không khớp dữ liệu đã cấp; kết quả đã bị chặn.",
    "MISSING_SOURCE_GUARD": "Thiếu mô tả lúc đặt nhưng AI chưa dừng đúng quy tắc; kết quả đã bị chặn.",
    "SNAPSHOT_REQUIRED": "AI chưa dẫn mô tả lúc đặt; kết quả đã bị chặn.",
    "SOURCE_PRESENCE_MISMATCH": "AI báo thiếu nguồn dù hồ sơ có mô tả lúc đặt; kết quả đã bị chặn. Hãy thử lại hoặc chọn model :free khác.",
    "MODEL_REFUSAL": "Model từ chối xử lý hồ sơ mẫu. Hãy thử lại hoặc chọn model :free khác.",
    "PROVIDER_TIMEOUT": "OpenRouter không trả lời trong thời gian chờ. Hãy thử lại sau.",
    "PROVIDER_CONNECTION": "Không kết nối được OpenRouter. Kiểm tra mạng rồi thử lại.",
    "EVIDENCE_SAVE_FAILED": "Đã nhận kết quả AI nhưng không lưu được bằng chứng. Kiểm tra quyền ghi thư mục prototype/evidence.",
    "PROVIDER_401": "OpenRouter không chấp nhận API key. Kiểm tra .env rồi khởi động lại máy chủ.",
    "PROVIDER_402": "Tài khoản không đáp ứng điều kiện của endpoint. Kiểm tra cấu hình model miễn phí trên OpenRouter.",
    "PROVIDER_404": "Hiện không có endpoint phù hợp cho model này. Thử lại sau hoặc chọn model :free khác.",
    "PROVIDER_429": "Model miễn phí đang giới hạn lượt gọi. Chờ rồi thử lại; ứng dụng không chuyển sang model trả phí.",
}


def create_app(*, key=None, model=None, transport=None, evidence_dir=None):
    key = os.getenv("OPENROUTER_API_KEY", "") if key is None else key
    model = model or os.getenv("OPENROUTER_MODEL", "openrouter/free")
    if model != "openrouter/free" and not re.fullmatch(r"[a-zA-Z0-9_.:/-]+:free", model):
        raise ValueError("Chỉ cho phép openrouter/free hoặc model có hậu tố :free.")
    evidence_dir = Path(evidence_dir) if evidence_dir is not None else ROOT / "evidence"
    token = secrets.token_urlsafe(32)
    busy = False
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        host = request.headers.get("host", "")
        origin = request.headers.get("origin")
        if not re.fullmatch(r"127\.0\.0\.1:\d+", host) or (origin and origin != f"http://{host}"):
            response = JSONResponse({"error": "Chỉ chấp nhận yêu cầu cùng nguồn tại 127.0.0.1."}, status_code=403)
        else:
            response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/api/config")
    async def config():
        return {"configured": bool(key), "model": model, "token": token}

    @app.get("/")
    @app.get("/index.html")
    async def index():
        return FileResponse(ROOT / "index.html", media_type="text/html")

    @app.get("/bonus.js")
    async def bonus_script():
        return FileResponse(ROOT / "bonus.js", media_type="text/javascript")

    @app.post("/api/analyze")
    async def analyze_request(request: Request):
        nonlocal busy
        if not secrets.compare_digest(request.headers.get("x-demo-token", ""), token) or not request.headers.get("content-type", "").startswith("application/json"):
            return JSONResponse({"error": "Hãy tải lại trang demo."}, status_code=403)
        if not key:
            return JSONResponse({"error": "Chưa cấu hình OPENROUTER_API_KEY ở máy chủ. Chưa có lời gọi AI thật."}, status_code=503)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 2048:
                return JSONResponse({"error": "Dữ liệu quá lớn."}, status_code=413)
        try:
            data = make_input(json.loads(body))
        except (ValueError, TypeError, KeyError):
            return JSONResponse({"error": "Chỉ chấp nhận lựa chọn S01/S02 và cờ dữ liệu mẫu."}, status_code=400)
        if busy:
            return JSONResponse({"error": "Đang xử lý một yêu cầu. Vui lòng đợi."}, status_code=429)
        busy = True
        try:
            started = perf_counter()
            output = await analyze(data, key=key, model=model, transport=transport)
            record = {
                "kind": "live_openrouter_response", "run_id": str(uuid4()),
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "duration_ms": round((perf_counter() - started) * 1000),
                "requested_model": model, "input": data, **output, "actions_executed": [],
            }
            try:
                evidence_dir.mkdir(parents=True, exist_ok=True)
                with (evidence_dir / f"{record['run_id']}.json").open("x", encoding="utf-8") as log:
                    json.dump(record, log, ensure_ascii=False, indent=2)
                    log.write("\n")
            except OSError as error:
                raise ValueError("EVIDENCE_SAVE_FAILED") from error
            return record
        except Exception as error:
            # Không trả về khóa, headers, thông báo provider hoặc traceback.
            if isinstance(error, httpx.TimeoutException):
                code = "PROVIDER_TIMEOUT"
            elif isinstance(error, httpx.RequestError):
                code = "PROVIDER_CONNECTION"
            else:
                code = str(error) if str(error) in ERROR_MESSAGES or re.fullmatch(r"PROVIDER_\d+", str(error)) else "ANALYSIS_FAILED"
            message = ERROR_MESSAGES.get(code, "Không nhận được kết quả AI hợp lệ. Chưa thực hiện hành động tiền nào.")
            return JSONResponse({"error": message, "code": code}, status_code=502)
        finally:
            busy = False

    return app


def main():
    load_dotenv(ROOT.parent / ".env", override=False)
    port = int(os.getenv("PORT", "3000"))
    print(f"Demo: http://127.0.0.1:{port} · OpenRouter key: {'configured' if os.getenv('OPENROUTER_API_KEY') else 'missing'}")
    uvicorn.run(create_app(), host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
