import subprocess
import sys
import paramiko

def get_load(ip, ssh_key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root', key_filename=ssh_key_path)
    stdin, stdout, stderr = ssh.exec_command("uptime | awk -F'load average:' '{ print $2 }' | cut -d',' -f1")
    load = float(stdout.read().decode().strip())
    ssh.close()
    return load

def main():
    if len(sys.argv) != 2:
        print("Usage: python deploy_postgres.py ip1 ip2")
        sys.exit(1)

    servers = sys.argv[1].split(',')
    ssh_key = "~/.ssh/id_rsa"

    print("Checking server loads...")
    loads = {ip: get_load(ip, ssh_key) for ip in servers}
    target_host = min(loads, key=loads.get)

    print(f"Installing PostgreSQL on: {target_host}")

    subprocess.run([
        "ansible-playbook",
        "playbook.yml",
        "-i", f"{target_host},",
        "-u", "root",
        "--private-key", ssh_key,
        "--extra-vars", f"target_host={target_host} peer_host={servers[1] if servers[0] == target_host else servers[0]}"
    ])


if __name__ == "__main__":
    main()
