from typing import Any, ContextManager, NamedTuple

from ._common import (
    FREEBSD as FREEBSD,
    NETBSD as NETBSD,
    OPENBSD as OPENBSD,
    AccessDenied as AccessDenied,
    NoSuchProcess as NoSuchProcess,
    ZombieProcess as ZombieProcess,
    conn_tmap as conn_tmap,
    conn_to_ntuple as conn_to_ntuple,
    memoize as memoize,
    usage_percent as usage_percent,
)

__extra__all__: Any
PROC_STATUSES: Any
TCP_STATUSES: Any
PAGESIZE: Any
AF_LINK: Any
HAS_PER_CPU_TIMES: Any
HAS_PROC_NUM_THREADS: Any
HAS_PROC_OPEN_FILES: Any
HAS_PROC_NUM_FDS: Any
kinfo_proc_map: Any

class svmem(NamedTuple):
    total: Any
    available: Any
    percent: Any
    used: Any
    free: Any
    active: Any
    inactive: Any
    buffers: Any
    cached: Any
    shared: Any
    wired: Any

class scputimes(NamedTuple):
    user: Any
    nice: Any
    system: Any
    idle: Any
    irq: Any

class pmem(NamedTuple):
    rss: Any
    vms: Any
    text: Any
    data: Any
    stack: Any

pfullmem = pmem

class pcputimes(NamedTuple):
    user: Any
    system: Any
    children_user: Any
    children_system: Any

class pmmap_grouped(NamedTuple):
    path: Any
    rss: Any
    private: Any
    ref_count: Any
    shadow_count: Any

class pmmap_ext(NamedTuple):
    addr: Any
    perms: Any
    path: Any
    rss: Any
    private: Any
    ref_count: Any
    shadow_count: Any

class sdiskio(NamedTuple):
    read_count: Any
    write_count: Any
    read_bytes: Any
    write_bytes: Any
    read_time: Any
    write_time: Any
    busy_time: Any

def virtual_memory(): ...
def swap_memory(): ...
def cpu_times(): ...
def per_cpu_times(): ...
def cpu_count_logical(): ...
def cpu_count_physical(): ...
def cpu_stats(): ...
def disk_partitions(all: bool = ...): ...

disk_usage: Any
disk_io_counters: Any
net_io_counters: Any
net_if_addrs: Any

def net_if_stats(): ...
def net_connections(kind): ...
def sensors_battery(): ...
def sensors_temperatures(): ...
def cpu_freq(): ...
def boot_time(): ...
def users(): ...
def pids(): ...
def pid_exists(pid): ...
def is_zombie(pid): ...
def wrap_exceptions(fun): ...
def wrap_exceptions_procfs(inst) -> ContextManager[None]: ...

class Process:
    pid: Any
    def __init__(self, pid) -> None: ...
    def oneshot(self): ...
    def oneshot_enter(self) -> None: ...
    def oneshot_exit(self) -> None: ...
    def name(self): ...
    def exe(self): ...
    def cmdline(self): ...
    def environ(self): ...
    def terminal(self): ...
    def ppid(self): ...
    def uids(self): ...
    def gids(self): ...
    def cpu_times(self): ...
    def cpu_num(self): ...
    def memory_info(self): ...
    memory_full_info: Any
    def create_time(self): ...
    def num_threads(self): ...
    def num_ctx_switches(self): ...
    def threads(self): ...
    def connections(self, kind: str = ...): ...
    def wait(self, timeout: Any | None = ...): ...
    def nice_get(self): ...
    def nice_set(self, value): ...
    def status(self): ...
    def io_counters(self): ...
    def cwd(self): ...
    class nt_mmap_grouped(NamedTuple):
        path: Any
        rss: Any
        private: Any
        ref_count: Any
        shadow_count: Any
    class nt_mmap_ext(NamedTuple):
        addr: Any
        perms: Any
        path: Any
        rss: Any
        private: Any
        ref_count: Any
        shadow_count: Any
    def open_files(self): ...
    def num_fds(self): ...
    def cpu_affinity_get(self): ...
    def cpu_affinity_set(self, cpus) -> None: ...
    def memory_maps(self): ...
    def rlimit(self, resource, limits: Any | None = ...): ...
