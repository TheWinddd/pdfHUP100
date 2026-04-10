import streamlit as st
import os, time, subprocess, sys, io, zipfile, requests, threading, shutil, queue

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="VQB trường Dờ", page_icon="📚", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; color: #e8e6e0; font-family: 'Syne', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%),
        #0a0a0f;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
.block-container { max-width: 720px; padding: 3rem 2rem 4rem; }

.hero { text-align: center; padding: 2.5rem 0 2rem; }
.hero-badge {
    display: inline-block; font-family: 'DM Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.2em; color: #ff8c32;
    border: 1px solid rgba(255,140,50,0.3); border-radius: 2px;
    padding: 0.3rem 0.8rem; margin-bottom: 1.2rem; text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2.4rem, 6vw, 3.6rem); font-weight: 800;
    line-height: 1.05; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 40%, #ff8c32 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.8rem;
}
.hero p { color: rgba(232,230,224,0.5); font-size: 1rem; }
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.25), transparent);
    margin: 1.8rem 0;
}
.card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1.8rem; margin-bottom: 1.2rem;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important; color: #e8e6e0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.85rem !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,140,50,0.5) !important;
    box-shadow: 0 0 0 2px rgba(255,140,50,0.08) !important;
}
[data-testid="stTextInput"] label {
    color: rgba(232,230,224,0.6) !important; font-size: 0.75rem !important;
    font-family: 'DM Mono', monospace !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #ff8c32 0%, #ff4e1e 100%) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.95rem !important; padding: 0.75rem 2rem !important;
}
[data-testid="stButton"] button:disabled {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(232,230,224,0.3) !important;
}
[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: rgba(255,140,50,0.12) !important; color: #ff8c32 !important;
    border: 1px solid rgba(255,140,50,0.35) !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
    font-size: 0.9rem !important; padding: 0.7rem 2rem !important;
}
.status-box {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
    font-family: 'DM Mono', monospace;
}
.status-label { color: rgba(232,230,224,0.4); font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.4rem; }
.status-value { color: #e8e6e0; font-size: 0.88rem; }
.status-value.accent { color: #ff8c32; font-size: 1.4rem; }
.log-box {
    background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px; padding: 1rem 1.2rem; font-family: 'DM Mono', monospace;
    font-size: 0.75rem; color: rgba(232,230,224,0.55);
    max-height: 220px; overflow-y: auto; line-height: 1.8;
}
.log-ok  { color: #5dde8a; }
.log-err { color: #ff5555; }
.log-info{ color: #ff8c32; }
.success-banner {
    background: linear-gradient(135deg, rgba(93,222,138,0.1), rgba(93,222,138,0.04));
    border: 1px solid rgba(93,222,138,0.25); border-radius: 10px;
    padding: 1.6rem 1.8rem; text-align: center; margin: 1.2rem 0;
}
.success-banner h3 { font-size: 1.2rem; font-weight: 700; color: #5dde8a; margin-bottom: 0.3rem; }
.success-banner p { color: rgba(232,230,224,0.5); font-family: 'DM Mono', monospace; font-size: 0.78rem; }
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #ff8c32, #ff4e1e) !important; border-radius: 4px !important;
}
[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.06) !important; border-radius: 4px !important; height: 6px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Global queue (thread-safe communication) ──────────────────────────────────
if "msg_queue" not in st.session_state:
    st.session_state.msg_queue = queue.Queue()

# ── Session state defaults ────────────────────────────────────────────────────
DEFAULTS = {
    "running": False, "done": False,
    "pdf_bytes": None, "pdf_name": "tai_lieu.pdf",
    "log": [], "progress": 0.0,
    "total_pages": 0, "captured": 0,
    "start_time": None, "elapsed": 0.0, "error": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Worker (NO st.* calls — only queue) ──────────────────────────────────────
def run_download(url: str, out_dir: str, q: queue.Queue):
    def send(kind, msg):
        q.put(("log", kind, msg))

    def push(**kwargs):
        q.put(("state", kwargs))

    try:
        # ── Chromium setup ─────────────────────────────────────────────────────
        send("info", "Kiểm tra Chromium…")

        chrome_binary = None
        for p in ['/usr/bin/chromium', '/usr/bin/chromium-browser']:
            if os.path.exists(p):
                chrome_binary = p
                break
        if not chrome_binary:
            r = subprocess.run(
                "which chromium || which chromium-browser",
                shell=True, capture_output=True, text=True)
            chrome_binary = r.stdout.strip() or None

        chromedriver_path = None

        if chrome_binary:
            ver_str = subprocess.run(
                [chrome_binary, "--version"], capture_output=True, text=True
            ).stdout.strip()
            send("ok", f"Chromium: {ver_str}")

            # ── ChromeDriver (installed via packages.txt) ─────────────────────
            for p in ['/usr/bin/chromedriver', '/usr/lib/chromium/chromedriver']:
                if os.path.exists(p):
                    chromedriver_path = p
                    break
            if not chromedriver_path:
                r = subprocess.run("which chromedriver", shell=True,
                                   capture_output=True, text=True)
                chromedriver_path = r.stdout.strip() or None

            if chromedriver_path:
                send("ok", f"ChromeDriver: {chromedriver_path}")
            else:
                send("info", "ChromeDriver không tìm thấy, dùng Selenium Manager…")
        else:
            send("info", "Không thấy Chromium hệ thống, thử Selenium Manager…")

        # ── WebDriver ─────────────────────────────────────────────────────────
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1200,1600")
        if chrome_binary:
            opts.binary_location = chrome_binary

        send("info", "Khởi tạo WebDriver…")
        driver = (
            webdriver.Chrome(service=Service(chromedriver_path), options=opts)
            if chromedriver_path
            else webdriver.Chrome(options=opts)
        )
        send("ok", "WebDriver OK!")

        try:
            send("info", "Mở tài liệu…")
            driver.get(url)
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "PDFViewerLB_CurrentPageImage"))
                )
                send("ok", "Trang tài liệu load xong!")
            except:
                send("err", "Timeout chờ element, tiếp tục…")

            # Đếm trang
            try:
                panel = driver.find_element(By.ID, "PDFViewerLB_BookmarkPanel")
                total = len(panel.find_elements(By.TAG_NAME, "li"))
            except:
                total = 86
            send("ok", f"Tổng số trang: {total}")
            push(total_pages=total)

            image_paths = []
            t0 = time.time()

            for i in range(total):
                png = None
                try:
                    img_el = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "PDFViewerLB_CurrentPageImage"))
                    )
                    png = img_el.screenshot_as_png
                except Exception as e:
                    send("err", f"Trang {i+1}: lỗi lấy – {e}")

                if png:
                    path = os.path.join(out_dir, f"page_{i+1:03d}.png")
                    with open(path, "wb") as f:
                        f.write(png)
                    image_paths.append(path)

                push(captured=i+1, progress=(i+1)/total, elapsed=time.time()-t0)

                if i < total - 1:
                    clicked = False
                    for st_, sv in [
                        (By.CSS_SELECTOR, "input[title='Trang sau']"),
                        (By.XPATH, "//input[@title='Next page']"),
                    ]:
                        try:
                            driver.find_element(st_, sv).click()
                            time.sleep(2)
                            clicked = True
                            break
                        except:
                            continue
                    if not clicked:
                        send("err", f"Không qua được trang {i+2}. Dừng.")
                        break

            send("ok", f"Đã lấy {len(image_paths)}/{total} trang.")

            # ── Tạo PDF ───────────────────────────────────────────────────────
            send("info", "Đang tạo PDF…")
            image_paths.sort()
            pdf_path = os.path.join(out_dir, "output.pdf")
            try:
                import img2pdf
                with open(pdf_path, "wb") as f:
                    f.write(img2pdf.convert(image_paths))
                send("ok", "PDF tạo xong (img2pdf)!")
            except Exception as e:
                send("err", f"img2pdf lỗi ({e}), thử PIL…")
                from PIL import Image as PILImage
                imgs = [PILImage.open(p).convert("RGB") for p in image_paths]
                imgs[0].save(pdf_path, save_all=True, append_images=imgs[1:])
                send("ok", "PDF tạo xong (PIL)!")

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            push(pdf_bytes=pdf_bytes, elapsed=time.time()-t0, done=True)

        finally:
            try: driver.quit()
            except: pass

    except Exception as e:
        send("err", f"LỖI NGHIÊM TRỌNG: {e}")
        push(error=str(e), done=True)
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)
        push(running=False)
        q.put(("done", None))


# ── Drain queue → session_state (safe, runs in main thread) ──────────────────
def drain_queue():
    q = st.session_state.msg_queue
    while True:
        try:
            item = q.get_nowait()
        except queue.Empty:
            break
        if item[0] == "log":
            _, kind, msg = item
            st.session_state.log.append((kind, msg))
        elif item[0] == "state":
            for k, v in item[1].items():
                st.session_state[k] = v


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Trường Dờ Document Downloader</div>
    <h1>Tải Tài Liệu<br>PDF trường Dờ</h1>
    <p>Nhập link tài liệu của con vợ vào phía dưới :v</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Form ──────────────────────────────────────────────────────────────────────

doc_url = st.text_input(
    "URL/Link Tài Liệu - sau khi nhập ấn enter",
    placeholder="https://elib.hup.edu.vn/opacdigital/ViewPDF.aspx?...",
    disabled=st.session_state.running,
)
pdf_name = st.text_input(
    "Đặt tên file PDF (tuỳ chọn)",
    value=st.session_state.pdf_name,
    disabled=st.session_state.running,
)
if not pdf_name.endswith(".pdf"):
    pdf_name += ".pdf"
st.session_state.pdf_name = pdf_name

btn_label = "⏳ Đang xử lý…" if st.session_state.running else "🚀 Bắt đầu tải"
start_btn = st.button(btn_label, disabled=st.session_state.running or not doc_url.strip())


# ── Start ─────────────────────────────────────────────────────────────────────
if start_btn and doc_url.strip() and not st.session_state.running:
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.session_state.msg_queue  = queue.Queue()
    st.session_state.running    = True
    st.session_state.start_time = time.time()

    out_dir = f"/tmp/elib_{int(time.time())}"
    os.makedirs(out_dir, exist_ok=True)

    threading.Thread(
        target=run_download,
        args=(doc_url.strip(), out_dir, st.session_state.msg_queue),
        daemon=True,
    ).start()
    st.rerun()

# ── Live panel ────────────────────────────────────────────────────────────────
if st.session_state.running or st.session_state.done:
    drain_queue()

    elapsed = st.session_state.elapsed
    if st.session_state.running and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time

    h = int(elapsed // 3600)
    m = int((elapsed % 3600) // 60)
    s = int(elapsed % 60)
    timer_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
    pct = int(st.session_state.progress * 100)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="status-box">
            <div class="status-label">Thời gian</div>
            <div class="status-value accent">{timer_str}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="status-box">
            <div class="status-label">Trang đã lấy</div>
            <div class="status-value accent">{st.session_state.captured} / {st.session_state.total_pages or "?"}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="status-box">
            <div class="status-label">Tiến độ</div>
            <div class="status-value accent">{pct}%</div>
        </div>""", unsafe_allow_html=True)

    st.progress(st.session_state.progress)

    if st.session_state.log:
        log_html = "".join(
            f'<div class="{"log-ok" if k=="ok" else "log-err" if k=="err" else "log-info"}">'
            f'{"✓" if k=="ok" else "✗" if k=="err" else "›"} {m}</div>'
            for k, m in st.session_state.log[-40:]
        )
        st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)

    if st.session_state.done and st.session_state.pdf_bytes:
        size_mb = len(st.session_state.pdf_bytes) / 1024 / 1024
        st.markdown(f"""<div class="success-banner">
            <div style="font-size:2rem;margin-bottom:.4rem">✅</div>
            <h3>Hoàn thành!</h3>
            <p>{st.session_state.captured} trang · {size_mb:.2f} MB · {timer_str}</p>
        </div>""", unsafe_allow_html=True)
        st.download_button(
            label=f"⬇️  Tải xuống {st.session_state.pdf_name}",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.pdf_name,
            mime="application/pdf",
        )
        if st.button("🔄 Tải tài liệu khác"):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.session_state.msg_queue = queue.Queue()
            st.rerun()

    elif st.session_state.done and st.session_state.error:
        st.error(f"❌ Lỗi: {st.session_state.error}")
        if st.button("🔄 Thử lại"):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.session_state.msg_queue = queue.Queue()
            st.rerun()

    if st.session_state.running:
        time.sleep(1)
        st.rerun()