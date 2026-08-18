#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键双发：本地变更 → ①GitHub 仓库（english-teaching-production）②飞书看板
================================================================
依据《GPT对话流程规范_20260806.md》§步骤2 同步范围：
  - 00_格式规范/  全部
  - 00_工具/      正式工具 + 词库 JSON（不含 _/fix_/check_ 临时脚本、bak、html/docx/txt 样例产物）
  - 00_总规划/    全部（不含 06_归档/、zip、_temp_*.html）
  - README.md / 样例课件 为仓库既有内容，本脚本只增不删
同步方式：本地 → staging 仓库（C:\\Users\\郭永涛\\AppData\\Local\\Temp\\eng-teaching-up），
         git commit + push origin main，再跑 feishu_sync.py 刷飞书。

用法：
    python publish_all.py --dry   # 只同步文件到 staging + 显示 git status，不提交不推送
    python publish_all.py         # 同步 + commit + push + 刷飞书
"""

import os
import shutil
import subprocess
import sys

BASE = r"D:\英语教学"
STAGING = r"C:\Users\郭永涛\AppData\Local\Temp\eng-teaching-up"
TOOL_DIR = os.path.join(BASE, "00_工具")
FEISHU_SYNC = os.path.join(TOOL_DIR, "ops", "feishu_sync.py")

# ---------- 00_工具 过滤 ----------
# 一次性调试/工具脚本（不以 _/fix_/check_ 开头、但属临时性质）不入库
ONEOFF_TOOLS = {
    "batch_diff_retrofit.py", "batch_patch_interaction.py", "build_all.py",
    "redistribute.py", "redistribute2.py", "redistribute3.py",
    "redistribute_answers.py", "repair_loop.py", "scan_status.py",
    "reissue_l17_l18.py", "build_state.json",
    # 2026-08-10 新增：单次验收脚本（非正式生成器/验证器）不入库
    "verify_guard_v1.py", "verify_LMX_L06_L10.py",
}

def is_formal_tool(fname):
    if fname.startswith(("_", "fix_", "check_")):
        return False
    if ".bak" in fname:
        return False
    if fname in ONEOFF_TOOLS:
        return False
    return fname.endswith(".py") or fname.endswith(".json")

def sync_tools(src, dst):
    """00_工具 顶层文件级同步（仅正式工具+词库 JSON）。"""
    os.makedirs(dst, exist_ok=True)
    copied = []
    for fname in sorted(os.listdir(src)):
        fp = os.path.join(src, fname)
        if os.path.isfile(fp) and is_formal_tool(fname):
            shutil.copy2(fp, os.path.join(dst, fname))
            copied.append(fname)
    return copied

# ---------- 00_总规划 / 00_格式规范 递归同步 ----------
EXCLUDE_DIRS_TOP = {"06_归档", "_GPT交互菜单包_20260805"}

def should_skip(fname):
    # 临时/调试残留（_ 开头、_temp_、zip）不入库
    if fname.startswith("_"):
        return True
    if "备份" in fname or "旧件" in fname:
        return True
    return fname.lower().endswith(".zip")

def sync_tree(src, dst, excluded_top_dirs):
    """递归复制，跳过 excluded_top_dirs（仅顶层生效）与 _temp_*/zip。"""
    os.makedirs(dst, exist_ok=True)
    copied = []
    for fname in sorted(os.listdir(src)):
        if should_skip(fname):
            continue
        sp = os.path.join(src, fname)
        dp = os.path.join(dst, fname)
        if os.path.isdir(sp):
            if fname in excluded_top_dirs:
                continue
            copied.extend(sync_tree(sp, dp, set()))
        else:
            shutil.copy2(sp, dp)
            copied.append(os.path.relpath(dp, dst))
    return copied

# ---------- 主流程 ----------
def git(*args, cwd):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr

def main():
    dry = "--dry" in sys.argv

    # 1) 同步到 staging
    all_copied = []

    def _sync_pydir(sub):
        """同步 00_工具 的子目录（engine/build/ops）正式 .py。"""
        src = os.path.join(TOOL_DIR, sub)
        dst = os.path.join(STAGING, "00_工具", sub)
        if not os.path.isdir(src):
            return
        os.makedirs(dst, exist_ok=True)
        for fname in sorted(os.listdir(src)):
            fp = os.path.join(src, fname)
            if os.path.isfile(fp) and is_formal_tool(fname):
                shutil.copy2(fp, os.path.join(dst, fname))
                all_copied.append(os.path.join(sub, fname))

    # 00_工具 顶层正式工具（P1-2 起仅数据维护工具；数据 JSON 已迁 01_数据）
    all_copied += sync_tools(TOOL_DIR, os.path.join(STAGING, "00_工具"))
    # 00_工具 子目录（engine/build/ops）
    for sub in ("engine", "build", "ops"):
        _sync_pydir(sub)
    # 01_数据（content/banks/schemas，P1-2 起）
    all_copied += sync_tree(os.path.join(BASE, "01_数据"),
                            os.path.join(STAGING, "01_数据"),
                            set())
    all_copied += sync_tree(os.path.join(BASE, "00_总规划"),
                            os.path.join(STAGING, "00_总规划"),
                            EXCLUDE_DIRS_TOP)
    all_copied += sync_tree(os.path.join(BASE, "00_格式规范"),
                            os.path.join(STAGING, "00_格式规范"),
                            set())

    print(f"同步到 staging：{len(all_copied)} 个文件")
    rc, out, err = git("status", "--short", cwd=STAGING)
    print("--- git status --short ---")
    print(out if out.strip() else "(无变更)")

    if dry:
        print("\n[--dry] 不提交不推送。")
        return

    # 2) commit + push
    rc, out, err = git("add", "-A", cwd=STAGING)
    if rc != 0:
        print("git add 失败:", err[:500]); sys.exit(1)
    rc, out, err = git("commit", "-m", "流水线一键双发：同步规范/工具/命令/交付记录", cwd=STAGING)
    if rc != 0:
        if "nothing to commit" in (out + err):
            print("无提交内容（staging 与仓库一致）")
        else:
            print("git commit 失败:", err[:500]); sys.exit(1)
    else:
        print("已提交:", out.strip().splitlines()[-1] if out.strip() else "ok")
    rc, out, err = git("push", "origin", "main", cwd=STAGING)
    if rc != 0:
        print("git push 失败:", err[:600]); sys.exit(1)
    print("已 push origin main:", (out or err).strip().splitlines()[-1])

    # 3) 刷飞书看板
    print("\n--- feishu_sync.py sync ---")
    r = subprocess.run([sys.executable, FEISHU_SYNC, "sync"],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(r.stdout)
    if r.returncode != 0:
        print("feishu_sync 失败:", r.stderr[:500]); sys.exit(1)
    print("\n完成：GitHub 已更新 + 飞书看板已刷新")

if __name__ == "__main__":
    main()
