import subprocess
import threading
import os
import sys
from typing import Optional

_proc: Optional[subprocess.Popen] = None
_process_thread: Optional[threading.Thread] = None
_stop_requested = threading.Event()

def _process_output(proc: subprocess.Popen):
    assert proc.stdout is not None
    try:
        for line in proc.stdout:
            if _stop_requested.is_set():
                break
            # print each line from tcpdump live
            print(line, end="")
    except Exception as e:
        # defensive: print error and exit reader
        print(f"[reader error] {e}", file=sys.stderr)
    finally:
        # ensure stream is drained/closed
        try:
            proc.stdout.close()
        except Exception:
            pass


def start_sniffer():
    global _proc, _process_thread, _stop_requested

    # if already running, do nothing
    if _proc is not None and _proc.poll() is None:
        print("Sniffer already running!", file=sys.stderr)
        return
    
    # clear any previous stop request
    _stop_requested.clear()

    cmd = ["tcpdump", "-l", "-n", "-vv"]

    print("Starting tcpdump... (Ctrl-C to stop)")
    print(" ".join(cmd))

    try :
        _proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except FileNotFoundError:
        print("Error: tcpdump not found. Install tcpdump and try again.", file=sys.stderr)
        _proc = None
        return
    except PermissionError:
        print("Permission denied: run as root (sudo) or give tcpdump necessary capabilities.", file=sys.stderr)
        _proc = None
        return
    except Exception as e:
        print(f"Failed to start tcpdump: {e}", file=sys.stderr)
        _proc = None
        return
    
    # start processing output
    _reader_thread = threading.Thread(target=_process_output, args=(_proc,), daemon=True)
    _reader_thread.start()

def stop_sniffer(timeout: float = 2.0):
    global _proc, _process_thread, _stop_requested

    if _proc is None or _proc.poll() is not None:
        print("Sniffer is not running!", file=sys.stderr)
        return

    print("Stopping sniffer...")

    # signal stop requested
    _stop_requested.set()

    try:
        # First try polite termination
        _proc.terminate()
    except Exception:
        pass

    # wait a short while
    try:
        _proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # if still alive, attempt to kill the whole process group (Unix)
        try:
            if hasattr(os, "killpg") and _proc.pid:
                os.killpg(os.getpgid(_proc.pid), 9)
            else:
                _proc.kill()
        except Exception as e:
            print(f"Failed to kill tcpdump: {e}", file=sys.stderr)

    # join reader thread
    if _reader_thread:
        _reader_thread.join(timeout=1.0)
        _reader_thread = None

    # clean up
    _proc = None
    _stop_requested.clear()
    print("tcpdump stopped.")