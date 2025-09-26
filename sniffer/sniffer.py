import subprocess

def start_sniffer():
    cmd = ["tcpdump", "-l", "-n", "-vv"]

    print("Starting tcpdump... (Ctrl-C to stop)")
    print(" ".join(cmd))

    # Start tcpdump process
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as proc:
        try:
            for line in proc.stdout:
                print(line, end="")   # print each tcpdump line as it arrives
        except KeyboardInterrupt:
            print("\nStopping...")
            proc.terminate()