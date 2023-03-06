# Connects to all BlueStacks devices that use Hyper-V (dynamic port!) via ADB and returns a DataFrame

## pip install bstconnect

```python

from bstconnect import connect_to_all_localhost_devices
df = connect_to_all_localhost_devices(
    adb_path="C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
    timeout=3,
    bluestacks_config=r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
)
print(df)

  localhost   product      model     device transport_id  status f_isroot f_root f_unroot bst_instance  num_threads  ppid memory_full_info    environ       name  cpu_percent num_ctx_switches   username    pid memory_info  memory_percent memory_maps        cwd  cpu_times  ionice  create_time    threads        exe open_files  nice io_counters status_proc cpu_affinity connections  num_handles    cmdline
0     52629  OnePlus3  ONEPLU...  OnePlus3T          1    device       ()     ()       ()    Pie64_2           97    8236  (12913...        {'ALLU...  HD-Pla...        0.1    (16629...        DESKTO...  14932  (12913...    0.188108       [(C:\W...   C:\Use...  (3.390...       2  1.6780...    [(1308...  C:\Pro...  [(C:\W...    32  (43543...     running   [0, 1,...           []        1324    [C:\\P...
1     53170  OnePlus5  ONEPLU...   OnePlus5          2    device       ()     ()       ()    Pie64_5          106    8236  (25288...        {'ALLU...  HD-Pla...        0.7    (13971...        DESKTO...   7568  (25288...    0.368370       [(C:\W...   C:\Use...  (2.25,...       2  1.6780...    [(1756...  C:\Pro...  [(C:\W...    32  (37717...     running   [0, 1,...    [(-1, ...        1400    [C:\\P...
2     53181  OnePlus5  ONEPLU...   OnePlus5          3    device       ()     ()       ()    Pie64_6           98    8236  (14550...        {'ALLU...  HD-Pla...        0.0    (13672...        DESKTO...   2108  (14550...    0.211957       [(C:\W...   C:\Use...  (1.921...       2  1.6780...    [(1415...  C:\Pro...  [(C:\W...    32  (36607...     running   [0, 1,...           []        1349    [C:\\P...
3     53361  OnePlus5  ONEPLU...   OnePlus5          4    device       ()     ()       ()    Pie64_3           98    8236  (14576...        {'ALLU...  HD-Pla...        0.0    (13222...        DESKTO...  10416  (14576...    0.212327       [(C:\W...   C:\Use...  (2.078...       2  1.6780...    [(1074...  C:\Pro...  [(C:\W...    32  (35549...     running   [0, 1,...           []        1351    [C:\\P...
4     55544  OnePlus5  ONEPLU...   OnePlus5         57    device       ()     ()       ()   Pie64_10           99    8236  (12911...        {'ALLU...  HD-Pla...        0.1    (28882...        DESKTO...  16604  (12911...    0.188072       [(C:\W...   C:\Use...  (1.312...       2  1.6780...    [(1644...  C:\Pro...  [(C:\W...    32  (13080...     running   [0, 1,...           []        1399    [C:\\P...
5     55554  a80ltexx   SM_A805N     a80lte         58    device       ()     ()       ()    Pie64_4           97    8236  (11723...        {'ALLU...  HD-Pla...        0.1    (28505...        DESKTO...   6440  (11723...    0.170769       [(C:\W...   C:\Use...  (1.390...       2  1.6780...    [(1566...  C:\Pro...  [(C:\W...    32  (12728...     running   [0, 1,...           []        1358    [C:\\P...

```