import subprocess


def download_aria2(url, download_path, connections=4):
    comand = (
        "aria2c --auto-file-renaming=false --allow-overwrite=true --continue=false -s"
        f' {connections} -x {connections} --dir="{download_path}" "{url}"'
    )
    subprocess.run(comand, shell=True)
