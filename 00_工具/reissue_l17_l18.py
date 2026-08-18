# -*- coding: utf-8 -*-
"""许颖嘉 L17/L18 课件重出（2026-08-03 起：生成器原生输出新体系，
本脚本仅负责 生成 → verify_v2 验收 → 备份旧件 → 替换交付）。

用法：
    python reissue_l17_l18.py            # 重出 L17 + L18
    python reissue_l17_l18.py 18         # 只重出第 18 课时
"""
import os, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_xyj_l17_l18 import build_lesson_17, build_lesson_18

JOBS = {
    17: dict(fn=build_lesson_17,
             out_dir="D:/英语教学/许颖嘉/第17课时/课件成品_网页PPT",
             fname="第17课时_课件_基础.html"),
    18: dict(fn=build_lesson_18,
             out_dir="D:/英语教学/许颖嘉/第18课时/课件成品_网页PPT",
             fname="第18课时_课件_基础.html"),
}


def _backup(path):
    """优先 .bak_20260803；已被占用则 .bak2/.bak3/... 递增。"""
    for i in range(1, 10):
        cand = path + (".bak_20260803" if i == 1 else ".bak%d_20260803" % i)
        if not os.path.exists(cand):
            return cand
    return path + ".bak_overflow_20260803"


def run_verify(tmp_path):
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "verify_v2.py"), tmp_path],
        capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    sys.stdout.write(out)
    return "PASS" in out


def main():
    args = [a for a in sys.argv[1:] if a.isdigit()]
    lessons = [int(a) for a in args] or sorted(JOBS.keys())
    results = {}
    for lesson in lessons:
        job = JOBS[lesson]
        print("== L%d 重出（生成器原生新体系）==" % lesson)
        html = job["fn"]()
        size = len(html.encode("utf-8"))
        print("  体积 %.1f KB" % (size / 1024.0))

        tmp = os.path.join(HERE, "_reissue_L%d_tmp.html" % lesson)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(html)
        ok = run_verify(tmp)
        print("  校验: %s" % ("PASS ✅" if ok else "⚠️ 未过 PASS（仍替换，见上）"))

        out_path = os.path.join(job["out_dir"], job["fname"])
        if os.path.exists(out_path):
            bak = _backup(out_path)
            os.replace(out_path, bak)
            print("  已备份旧件 → %s" % os.path.basename(bak))
        os.makedirs(job["out_dir"], exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        os.remove(tmp)
        print("  ✅ 已替换交付件：%s" % out_path)
        results[lesson] = {"bytes": size, "verify": ok}
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
