import os
import random
import re
import subprocess
import time
import pandas as pd
import kthread
import psutil
from capture_stdout_decorator import print_capture
from kthread_sleep import sleep
from a_pandas_ex_bstcfg2df import get_bst_config_df
from a_pandas_ex_regex_enhancements import pd_add_regex_enhancements
from flexible_partial import FlexiblePartialOwnName
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
pd_add_regex_enhancements()


def normp(adb_path):
    return os.path.normpath(adb_path)


def check_if_root(adb_path, serialnumber):
    adb_path = normp(adb_path)
    try:
        return (
            b"com.android"
            in subprocess.run(
                f"\"{adb_path}\" -s {serialnumber} shell su -c 'ls /data/data'",
                shell=True,
                capture_output=True,
            ).stdout
        )
    except Exception:
        return False


def root(adb_path, serialnumber):
    adb_path = normp(adb_path)
    try:

        return subprocess.run(
            f'"{adb_path}" -s {serialnumber} root',
            shell=True,
            capture_output=True,
        ).stdout.decode("utf-8", "ignore")
    except Exception:
        return pd.NA


def unroot(adb_path, serialnumber):
    adb_path = normp(adb_path)
    try:

        return subprocess.run(
            f'"{adb_path}" -s {serialnumber} unroot',
            shell=True,
            capture_output=True,
        ).stdout.decode("utf-8", "ignore")
    except Exception:
        return pd.NA


def execute_subprocess_multiple_commands_with_timeout_bin(
    cmd: str,
    subcommands: list,
    end_of_printline: str = "",
    print_output=True,
    timeout=None,
) -> list:
    if isinstance(subcommands, str):
        subcommands = [subcommands]
    elif isinstance(subcommands, tuple):
        subcommands = list(subcommands)
    popen = None
    t = None

    def run_subprocess(cmd):
        nonlocal t
        nonlocal popen

        def killer():
            sleep(timeout)
            kill_process()

        def kill_process():
            nonlocal popen

        DEVNULL = open(os.devnull, "wb")
        try:
            popen = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=False,
                stderr=DEVNULL,
                shell=False,
            )

            for subcommand in subcommands:
                if isinstance(subcommand, str):
                    subcommand = subcommand.rstrip("\n") + "\n"

                    subcommand = subcommand.encode()
                else:
                    subcommand = subcommand.rstrip(b"\n") + b"\n"

                popen.stdin.write(subcommand)

            popen.stdin.close()

            if timeout is not None:
                t = kthread.KThread(
                    target=killer, name=str(random.randrange(1, 100000000000))
                )
                t.start()

            for stdout_line in iter(popen.stdout.readline, b""):
                try:
                    yield stdout_line
                except Exception as Fehler:
                    continue
            popen.stdout.close()
            return_code = popen.wait()
        except Exception as Fehler:
            print(Fehler)
            try:
                popen.stdout.close()
                return_code = popen.wait()
            except Exception as Fehler:
                yield ""

    proxyresults = []
    try:
        for proxyresult in run_subprocess(cmd):
            proxyresults.append(proxyresult)
            if print_output:
                try:
                    print(f"{proxyresult!r}", end=end_of_printline)
                    print("")
                except Exception:
                    pass
    except KeyboardInterrupt:
        try:
            p = psutil.Process(popen.pid)
            p.kill()
            popen = None
        except Exception as da:
            print(da)

    try:
        if popen is not None:
            p = psutil.Process(popen.pid)
            p.kill()
    except Exception as da:
        pass

    try:
        if t is not None:
            if t.is_alive():
                t.kill()
    except Exception:
        pass
    return proxyresults


@print_capture(print_output=False, return_func_val=True)
def _connect_to_all_localhost_devices(
    adb_path,
    timeout=10,
    bluestacks_config=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
    start_server=False,
    reconnect=False,
):
    if start_server:
        subprocess.run([adb_path, "start-server"])

    if reconnect:
        (
            subprocess.run(
                f'"{adb_path}" reconnect offline',
                shell=True,
                capture_output=True,
            ).stdout.decode("utf-8", "ignore")
        )

    activeadb_pid = -1
    for p in psutil.process_iter():
        if p.name().lower() == "adb.exe":
            try:
                activeadb_pid = p.pid
            except Exception as fe:
                print(fe)
                continue

    df2 = get_bst_config_df(conffile=bluestacks_config)
    ports = sorted(
        list(
            set(
                df2.ds_regex_find_all(
                    regular_expression=r"\badb_port\b", line_by_line=True
                )
                .reset_index(1)
                .index.to_list()
            )
        )
    )
    ports = df2.loc[ports].aa_values_stripped.to_list()
    kth = [
        kthread.KThread(
            target=execute_subprocess_multiple_commands_with_timeout_bin,
            name=aca,
            args=(
                f"{adb_path} connect localhost:{aca}",
                [],
                "",
                False,
                timeout,
            ),
        )
        for aca in ports
    ]
    _ = [i.start() for i in kth if sleep(0.01) is None]
    timeoutfinal = timeout + time.time() + len(_) * 0.01
    while [True for i in kth if i.is_alive()]:
        if timeoutfinal < time.time():
            break
        sleep(0.1)

    if timeoutfinal < time.time():
        for ac in kth:
            try:
                if ac.is_alive():
                    ac.kill()
            except Exception as fe:
                print(fe)
                pass

    if activeadb_pid > -1:
        for p in psutil.process_iter():
            if p.name().lower() == "adb.exe":
                if p.pid != activeadb_pid:
                    try:
                        p.kill()
                    except Exception as fe:
                        print(fe)
                        continue

    co = subprocess.run([adb_path, "devices", "-l"], capture_output=True)
    co = [
        x
        for x in co.stdout.decode("utf-8", "ignore").splitlines()
        if "localhost:" in str(x).lower()
    ]
    # co1 = [x for x in co if x]
    co1 = co.copy()

    co = [re.findall(r"\b[^:\s]+:[^:\s]+\b", x) for x in co1]
    co2 = [
        [f"status:{y.strip()}" for y in re.findall(r"\s+\b[^:\s]+\b\s+", x)]
        for x in co1
    ]
    co = [x[0] + x[1] for x in list(zip(co, co2))]
    df = pd.DataFrame([[y.split(":", maxsplit=1) for y in x] for x in co])
    newcols = []
    for col in df:
        newcols.append(df[col].iloc[0][0])
        df[col] = df[col].ds_apply_ignore(pd.NA, lambda x: x[1])
        df[col] = df[col].str.strip()
    df.columns = newcols
    df["f_isroot"] = df["localhost"].ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            check_if_root, "()", True, adb_path, f"localhost:{x}"
        ),
    )
    df["f_root"] = df["localhost"].ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(root, "()", True, adb_path, f"localhost:{x}"),
    )

    df["f_unroot"] = df["localhost"].ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            unroot, "()", True, adb_path, f"localhost:{x}"
        ),
    )

    return df, df2


def connect_to_all_localhost_devices(
    adb_path,
    timeout=10,
    bluestacks_config=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
):
    df = _connect_to_all_localhost_devices(
        adb_path,
        timeout=timeout,
        bluestacks_config=bluestacks_config,
    )
    dfbstc = (
        df[0][1]
        .loc[df[0][1].aa_values_stripped.isin(df[0][0].localhost)]
        .drop_duplicates(subset="aa_values_stripped")
        .copy()
    )
    dfadb = df[0][0].copy()
    dfbstc.index = dfbstc.aa_values_stripped.__array__().copy()
    dfadb.index = dfadb.localhost.__array__().copy()
    df = pd.concat([dfadb, dfbstc], axis=1).reset_index(drop=True)
    df = df[
        [x for x in df.columns if not str(x).startswith("aa_") or str(x) == "aa_key_3"]
    ].copy()
    df = df.rename(columns={"aa_key_3": "bst_instance"})
    newcols = []
    allinfos = []
    for p in psutil.process_iter():
        try:
            if "HD-Player.exe" in p.name():
                allinfos.append(p.as_dict().items())
        except Exception:
            continue
    df2 = pd.DataFrame.from_records(allinfos)
    for col in df2:
        newcols.append(df2[col].iloc[0][0])
        df2[col] = df2[col].ds_apply_ignore(pd.NA, lambda x: x[1])

    df2.columns = newcols
    df2["bst_instance"] = df2.cmdline.ds_apply_ignore(
        pd.NA,
        lambda x: x[[ini + 1 for ini, xx in enumerate(x) if xx == "--instance"][0]],
    )
    df2 = df2.rename(columns={"status": "status_proc"})
    df3 = df.merge(df2, right_on="bst_instance", left_on="bst_instance").copy()
    return df3
